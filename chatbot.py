from openai import OpenAI
from config import systemPromptSemanticAgent
from config import systemPromptPickerAgent
from config import systemPromptChat
import os
from dotenv import load_dotenv
from dashscope import Assistants, Messages, Runs, Threads

# 加载环境变量
load_dotenv()
apiKey = os.getenv("API_KEY")
visualAgentAssistantId = os.getenv("visualAgentAssistantId")

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
        # print("运行结果:")
        # for msg in msgs['data'][::-1]:
        #     print("content: ", msg['content'][0]['text']['value'])
        # print("\n")
        # 提取最新的输出
        latest_output = ""
        if msgs and 'data' in msgs:
            latest_output = msgs['data'][0]['content'][0]['text']['value']  # 获取最后一条消息的文本内容

        return latest_output  # 返回最新的输出



# posterContent = ChatBot(systemPrompt=systemPromptPickerAgent, model="qwen-turbo")
# content = "品牌还有什么"
# posterContent.add_user_message(content)
# assistantOutput = posterContent.get_reply()
# print(assistantOutput)


# # 1223 Chatbot tested
# posterTalker = ChatBot(systemPrompt=systemPromptChat, model="qwen-turbo-latest")  

# 用户输入：介绍一下菲利普塔斯克的作品。

# 海报分析机器人输入：
# {
#   "highlighted": [
#     {
#       "id": 15,
#       "text": "后现代主义通过共享的美学语言将全球设计师团结在一起，日本的仓保史朗和法国的菲利普斯塔克等设计师的作品即展现出这种跨文化对话。",
#       "type": "文本内容",
#       "keywords": ["后现代主义", "跨文化对话", "设计师"]
#     }
#   ]
# },
# "Dialogue": "菲利普斯塔克是法国著名设计师，他的作品深受后现代主义影响，强调跨文化对话。他设计的许多作品不仅体现了对传统形式的颠覆，还融入了折衷主义和讽刺性的元素，这些都成为了后现代主义设计的重要特征。斯塔克的作品常常打破常规，展现了一种新的美学语言，这种语言超越了地域和文化的界限，吸引了全球范围内的关注。"
# }

# 知识点扩展机器人输入：
# {
#   "keyinfo": [
#     {
#       "id": 1,
#       "keyword": "菲利普·斯塔克",
#       "image": "19017.png",
#       "description": "法国著名设计师，他的设计风格融合后现代主义元素、跨文化对话，并以打破常规的美学语言闻名。其标志性作品包括1988年设计的Royalton酒店和1990年的Juicy Salif柠檬榨汁器。",
#       "otherinfo": ""
#     },
#     {
#       "id": 2,
#       "keyword": "后现代主义",
#       "image": "19009.png",
#       "description": "后现代主义设计强调趣味性与多元化，常通过对传统形式的解构融入折衷和讽刺的元素。",
#       "otherinfo": "起源于20世纪80年代"
#     },
#     {
#       "id": 3,
#       "keyword": "Royalton酒店",
#       "image": "19017.png",
#       "description": "由菲利普·斯塔克设计的皇家顿酒店，以浓厚的戏剧化风格和独特的后现代空间设计在纽约1988年成为里程碑。",
#       "otherinfo": ""
#     },
#     {
#       "id": 4,
#       "keyword": "Juicy Salif柠檬榨汁器",
#       "image": "19018.png",
#       "description": "由菲利普·斯塔克为Alessi设计的标志性柠檬榨汁器，展现了艺术和功能的融合。",
#       "otherinfo": "设计于1990年"
#     }
#   ],
#   "connections": [
#     {
#       "from": 1,
#       "to": 2,
#       "relationship": "影响来源"
#     },
#     {
#       "from": 1,
#       "to": 3,
#       "relationship": "作品展示"
#     },
#     {
#       "from": 1,
#       "to": 4,
#       "relationship": "作品展示"
#     }
#   ]
# }




# 请基于以上输入生成你对用户的回复：

# """
# posterTalker.add_user_message(content)
# assistantOutput = posterTalker.get_reply()
# print(assistantOutput)
# # posterTalker.add_user_message(content)
# # assistantOutput = posterTalker.get_reply()
# # print(assistantOutput)





# # 1223 QwenAssistant tested
# # 创建实例
# assistant_id = 'asst_0c9a8326-2d15-4aa6-96fd-ea4ff9fc87f0'
# workspace = 'llm-8iz1w0zj4paj6z85'
# api_key = 'sk-da762947f89040b0895a6099f807bf62'

# generator_assistant = QwenAssistant(assistant_id, workspace, api_key)

# # 调用方法
# a = generator_assistant.send_message('孟菲斯运动是由埃托雷·索特萨斯在1980年代初推广的，旨在打破传统设计界限，强调色彩和材料的大胆运用。它以鲜艳的色彩和独特的形式著称，这些设计作品让我们重新思考了日常物品的美学。')
# print(a)