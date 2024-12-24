from openai import OpenAI
from config import systemPromptSemanticAgent
from config import systemPromptPickerAgent
import os
import dashscope
from dashscope import Assistants, Messages, Runs, Threads
from config import visualAgentAssistantId

apiKey = os.getenv("apiKey")
visualAgentAssistantId = 'asst_0c9a8326-2d15-4aa6-96fd-ea4ff9fc87f0'

class ChatBot:
  def __init__(self, systemPrompt, model: str = "qwen-turbo-latest") -> None:
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


# 千问assistant，与openai assistant很类似，通过在playgroud创建和调教assistant，获取assistant_id，然后直接调用assistant_id进行对话
# 操作教程见notion/开发onepage/后端实现/低代码快速构建RAG应用那个链接
class QwenAssistant:
    def __init__(self, assistant_id, workspace, api_key):
        self.assistant = Assistants.retrieve(
            assistant_id=assistant_id,
            workspace=workspace,
            api_key=api_key
        )

    def send_message(self, message):
        # print(f"Query: {message}")

        # create thread.
        thread = Threads.create()
        # print(thread)

        # create a message.
        message_obj = Messages.create(thread.id, content=message)
        # print(message_obj)

        # create run
        run = Runs.create(thread.id, assistant_id=self.assistant.id)
        # print(run)

        # wait for run to complete or requires_action
        run_status = Runs.wait(run.id, thread_id=thread.id)
        # print(run_status)

        # get the thread messages.
        msgs = Messages.list(thread.id)
        print("运行结果:")
        for msg in msgs['data'][::-1]:
            print("content: ", msg['content'][0]['text']['value'])
        print("\n")

