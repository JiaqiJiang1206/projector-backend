from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from dotenv import load_dotenv
from config import systemPromptPoster, systemPromptNumber
from chatbot import ChatBot
import uvicorn
import sys
import asyncio
import os

# 将上一层文件夹添加到 Python 的搜索路径中
sys.path.append(os.path.abspath('..'))
from cosyvoice.cli.cosyvoice import CosyVoice
from cosyvoice.utils.file_utils import load_wav
import torchaudio

cosyvoice = CosyVoice('../pretrained_models/CosyVoice-300M-SFT', load_jit=True, load_onnx=False, fp16=True)
# sft usage
# print(cosyvoice.list_avaliable_spks())

# 加载环境变量
load_dotenv()

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

# 初始化两个实例
posterTalker = ChatBot(systemPrompt=systemPromptPoster)
numChooser = ChatBot(systemPrompt=systemPromptNumber)

class ChatRequest(BaseModel):
    content: str  # 用户当前输入的消息

class ChatAudioRequest(BaseModel):
    content: str  # 客户端要求转为语音的消息

class SendAudioRequest(BaseModel):
    content: int  # 客户端要求语音文件的索引
   
# 定义聊天接口
@app.post("/api/chat/poster")
async def chatPoster(request: ChatRequest):
  try:
    # print(request)
    posterTalker.add_user_message(request.content)
    assistantOutput = posterTalker.get_reply()
    print(assistantOutput)
    # 返回模型的回复
    return {"reply": assistantOutput}
  except Exception as e:
      print(f"Error: {e}")
      raise HTTPException(status_code=500, detail="Failed to generate response")

#语音接口，开始生成语音数据
@app.post("/api/chat/startaudio")
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
@app.post("/api/chat/sendaudio")
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
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)