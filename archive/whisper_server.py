from fastapi import FastAPI, UploadFile, Form
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import whisper
import torch
import uvicorn
import os

# 设置 GPU 环境变量，强制使用 GPU 1
os.environ["CUDA_VISIBLE_DEVICES"] = "1"

# 检查 GPU 可用性
device = "cuda" if torch.cuda.is_available() else "cpu"

# 加载 Whisper 模型
model = whisper.load_model("large", device=device)

app = FastAPI()

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有 HTTP 方法
    allow_headers=["*"],  # 允许所有 HTTP 头
)

@app.post("/transcribe/")
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

if __name__ == "__main__":
    uvicorn.run("whisper_server:app", host="0.0.0.0", port=8001)
