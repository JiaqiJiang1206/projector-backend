# from openai import OpenAI
# import os
# from dotenv import load_dotenv

# # 加载 .env 文件中的环境变量
# load_dotenv()

# client = OpenAI()

# #从playground中调用assistant
# assistant = client.beta.assistants.retrieve("asst_ZbD726O8gB1cQec9YEK0APjr")

# thread = client.beta.threads.create()

# message = client.beta.threads.messages.create(
# thread_id=thread.id,
# role="user",
# content="咱来聊聊后现代主义的国际影响吧"
# )

# run = client.beta.threads.runs.create_and_poll(
# thread_id=thread.id,
# assistant_id=assistant.id,
# instructions=""
# )

# if run.status == 'completed': 
#   messages = client.beta.threads.messages.list(
#     thread_id=thread.id
#   )
#   print(messages)
# else:
#   print(run.status)

from openai import OpenAI
from config import apiKey
from config import systemPromptPoster, systemPromptNumber

class ChatBot:
  def __init__(self, systemPrompt, model: str = "qwen-turbo") -> None:
    self.client = OpenAI(
        api_key=apiKey,
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    )
    self.model = model
    self.conversation_history = [
      {'role': 'system', 'content': systemPrompt}
    ]
  
  def add_user_message(self, content: str):
    """Add a user message to the conversation history."""
    self.conversation_history.append({'role': 'user', 'content': content})
  
  def get_reply(self) -> str:
    """Call the model and get a reply."""
    completion = self.client.chat.completions.create(
        model=self.model,
        messages=self.conversation_history,
    )
    assistant_output = completion.choices[0].message.content
    self.conversation_history.append({'role': 'assistant', 'content': assistant_output})
    return assistant_output
  
posterTalker = ChatBot(systemPrompt=systemPromptPoster) 
content = "我们来聊聊创意回收运动吧"
posterTalker.add_user_message(content)
assistantOutput = posterTalker.get_reply()
print(assistantOutput)