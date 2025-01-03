from fastapi import FastAPI, HTTPException, UploadFile, Form
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from dotenv import load_dotenv
from chatbot import ChatBot
from chatbot import QwenAssistant
import uvicorn
import sys
import asyncio
import os
import whisper
import torch
import dashscope
from search import Search
from config import systemPromptPickerAgent
from config import systemPromptChat

# 将上一层文件夹添加到 Python 的搜索路径中
sys.path.append(os.path.abspath('..'))
from cosyvoice.cli.cosyvoice import CosyVoice
from cosyvoice.utils.file_utils import load_wav
import torchaudio

cosyvoice = CosyVoice('../pretrained_models/CosyVoice-300M-SFT', load_jit=True, load_onnx=False, fp16=True)

# 加载环境变量
load_dotenv()
assistant_id = 'asst_0c9a8326-2d15-4aa6-96fd-ea4ff9fc87f0'
workspace = os.getenv("WORKSPACE")
api_key = os.getenv("API_KEY")
dashscope.api_key = api_key

# 设置 GPU 环境变量，强制使用 GPU 1
os.environ["CUDA_VISIBLE_DEVICES"] = "1"

# 检查 GPU 可用性
device = "cuda" if torch.cuda.is_available() else "cpu"

# 加载 Whisper 模型
model = whisper.load_model("large", device=device)

# 初始化 FastAPI 应用
app = FastAPI()

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有 HTTP 方法
    allow_headers=["*"],  # 允许所有 HTTP 头
)

# 初始化两个agent
PickerAgent = ChatBot(systemPrompt=systemPromptPickerAgent,model='qwen-plus')
ChatAgent = ChatBot(systemPrompt=systemPromptChat,model='qwen-turbo')
GeneratorAssistant = QwenAssistant(assistant_id, workspace, api_key)


class ChatRequest(BaseModel):
    content: str  # 用户当前输入的消息

class ChatAudioRequest(BaseModel):
    content: str  # 客户端要求转为语音的消息

class SendAudioRequest(BaseModel):
    content: int  # 客户端要求语音文件的索引

class PickerResponse(BaseModel):
    content: str  # Picker 的回复

class GeneratorResponse(BaseModel):
    user_input: str  # 用户语音输入的消息
    picker_description: str  # picker的回复-rawoutput_picker
    generator_output: str  # generator的回复-generator_output


   
# 定义picker接口
@app.post("/api/picker")
async def highlightPicker(request: ChatRequest):
  try:
    print(request)
    PickerAgent.add_user_message(request.content)
    assistantOutput = PickerAgent.get_reply()
    #
    chat_input = ""
    print(1)
    print(assistantOutput)
    output = Search(assistantOutput, '0_grouped.json')
    print(2)
    print(output)
    # 返回模型的回复
    return {"rawoutput_picker": output[0],
            "highlight_point": output[1]}
  except Exception as e:
      print(f"Error: {e}")
      raise HTTPException(status_code=500, detail="Failed to generate response")

#定义向前端请求picker回复并发送generator的输出
@app.post("/api/pickertogenerator")
async def pickertoGenerator(feedback: PickerResponse):
    try:
        print(f"Received feedback: {feedback.content}")
        # 从前端接收到的 picker 输出
        # assistant_data = json.loads(feedback.content)
        # 需要测测
        description = feedback.content
        generatoroutput = GeneratorAssistant.send_message(description)
        # 此处可以根据需求处理接收到的 rawoutput_picker
        # 比如存储到数据库或再次处理
        return {"generator_output": generatoroutput}
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Failed to process feedback")

#定义向前端请求picker回复并发送generator的输出
@app.post("/api/generatortochat")
async def generatortoChat(feedback: GeneratorResponse):
    try:
        # 从前端接收到的 picker 输出
        input_chat = f"""
        用户输入：{feedback.user_input}

        海报分析机器人输入：{feedback.picker_description}

        知识点扩展机器人输入：{feedback.generator_output}
        """
        print(input_chat)

        ChatAgent.add_user_message(input_chat)
        generatoroutput = ChatAgent.get_reply()
        # 此处可以根据需求处理接收到的 rawoutput_picker
        # 比如存储到数据库或再次处理
        return {"generator_output": generatoroutput}
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Failed to process feedback")

@app.post("/api/transcribe")
async def transcribe_audio(
    file: UploadFile, 
    language: str = Form("zh"), 
    initial_prompt: str = Form("请转录为简体中文。")
):
    """
    接受音频文件并返回转录文字
    """
    try:
        # 保存上传的音频文件
        audio_path = f"temp_{file.filename}"
        with open(audio_path, "wb") as audio_file:
            audio_file.write(await file.read())
        
        # 使用 Whisper 转录音频
        result = model.transcribe(
            audio_path,
            language=language,
            word_timestamps=True,
            initial_prompt=initial_prompt,
        )
        
        # 返回转录结果
        return JSONResponse(content={"text": result["text"], "segments": result["segments"]})
    
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

#语音接口，开始生成语音数据
@app.post("/api/startaudio")
async def start_audio(request: ChatAudioRequest):
  try:
    print(request.content)
    count = 0
    # change stream=True for chunk stream inference
    for i, j in enumerate(cosyvoice.inference_sft(request.content, '中文女', stream=False)):
        torchaudio.save('sft_{}.wav'.format(i), j['tts_speech'], 22050)
        count = i + 1
    print("生成了"+str(count)+"个音频文件")
    # 返回模型的回复
    return {"reply": count}
  except Exception as e:
      print(f"Error: {e}")
      raise HTTPException(status_code=500, detail="Failed to generate response")
  
async def delete_file(file_path: str):
    await asyncio.sleep(3)  # 模拟延迟
    if os.path.exists(file_path):
        os.remove(file_path)

# 定义一个接口返回音频文件
@app.post("/api/sendaudio")
async def get_audio(file_name: SendAudioRequest):
    file_path ='/home/aidealstudio/jjq/CosyVoice/server/sft_{}.wav'.format(file_name.content)
    print(file_path)
    try:
        # 检查文件是否存在
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="Audio file not found")
        # 先返回文件
        response = FileResponse(file_path, media_type="audio/wav")
        # 使用异步任务删除文件
        asyncio.create_task(delete_file(file_path))
        return response
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Failed to send file: {str(e)}")

# 测试根路径
@app.get("/")
async def root():
    return {"message": "Server is running!"}

# 启动服务（可选：uvicorn main:app --reload --port 8080 --host 0.0.0.0
if __name__ == "__main__":
    # export PYTHONPATH=../third_party/Matcha-TTS
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)