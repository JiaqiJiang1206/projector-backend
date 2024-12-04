from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from config import systemPromptPoster, systemPromptNumber
from chatbot import ChatBot
import json

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

# 定义聊天接口
@app.post("/api/chat/poster")
async def chatPoster(request: ChatRequest):
  try:
    print(request)
    posterTalker.add_user_message(request.content)
    assistantOutput = posterTalker.get_reply()
    
    # 返回模型的回复
    return {"reply": assistantOutput}
  except Exception as e:
      print(f"Error: {e}")
      raise HTTPException(status_code=500, detail="Failed to generate response")

# 测试根路径
@app.get("/")
async def root():
    return {"message": "Server is running!"}

# 启动服务（可选：使用 `uvicorn main:app --reload` 启动时无需这个部分）
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)