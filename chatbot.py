from openai import OpenAI
from config import systemPromptSemanticAgent
from config import systemPromptPickerAgent1, systemPromptPickerAgent2, systemPromptPickerAgent3
import os
from dotenv import load_dotenv
from dashscope import Assistants, Messages, Runs, Threads

# 加载环境变量
load_dotenv()
apiKey = os.getenv("sk-da762947f89040b0895a6099f807bf62")
visualAgentAssistantId = os.getenv("asst_0c9a8326-2d15-4aa6-96fd-ea4ff9fc87f0")

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


# systemPromptPickerAgent 测试
# posterContent = ChatBot(systemPrompt=systemPromptSemanticAgent, model="qwen-max-2024-09-19")
# content = '''
# 按照设计历史的海报主题19世纪90年代的设计历史内容设计的全球化浪潮，进行最贴近主题的分区，不要单纯按出现顺序分组。有的图片跟主题的id顺序不在一起，但你需要根据图片信息和你已知的设计历史的常识，来判断该图片最属于哪个小主题。

# [
#     {
#         "id": 0,
#         "text": "理性与工艺的变革"
#     },
#     {
#         "id": 1,
#         "text": "高技派风格的后示"
#     },
#     {
#         "id": 2,
#         "text": "高技派设计风格在1970年代兴起，其灵感源 于工业和技术的精简美学。建筑师如理查德 罗杰斯和诺曼-福斯特强调通过裸露的钢梁和 管道元素打造出功能至上的设计，这些作品不 仅实用，还极具视觉冲击力。此风格在室内设 计中延续，通过像罗德尼金斯曼的Omkstak 椅子这样标志性家具，使其成为那个时代的视 觉象征。"
#     },
#     {
#         "id": 3,
#         "text": "图1:1971年，罗德尼金斯曼为 OMK设计的Omkstak椅子"
#     },
#     {
#         "id": 4,
#         "text": "图2:1972年，理查德萨普尔大 Artemide设计的Tizio工作灯"
#     },
#     {
#         "id": 5,
#         "text": "工艺复兴与人体工程学"
#     },
#     {
#         "id": 6,
#         "text": "设计的社会职能"
#     },
#     {
#         "id": 7,
#         "text": "工艺复兴与人体工程学在70年代中叶并行发 展，设计强调与用户的物理和情感连接，一方 面响应高技派设计的冷感、设计师诵讨探卖传 统手工艺的价值和功能性家具如彼得奥普斯 维克的Balans Variable椅子，提升产品舒适 性与实用性。"
#     },
#     {
#         "id": 8,
#         "text": "设计的社会使命在20世纪70年代中期也受到关注，功能性和安 全性被置于设计的优先地位。以佩帕内克的《为真实世界设 计》为代表，倡导产品设计应保进人与人之间的互动和满足实 际需求，推动设计创新与社会责任的结合，形成设计的新标 准"
#     },
#     {
#         "id": 9,
#         "text": "电子时代的影响"
#     },
#     {
#         "id": 10,
#         "text": "电子技术自70年代起改变设计格 局，从电子游戏到移动通信设备普 及，如摩托罗拉\"砖块\"大哥大和柬 尼随身听问世标志便携式电子产品 设计革命。设计从空间拓展至数字 领域，定义现代生活新模式。"
#     },
#     {
#         "id": 11,
#         "text": "图4:1979年推出的首款察尼 随身听 (TPS-L2)"
#     },
#     {
#         "id": 12,
#         "text": "环保意识与手工艺"
#     },
#     {
#         "id": 13,
#         "text": "随着工艺复兴，环保意识逐渐影响设计实践，设计师察觉到小 规模生产所带来的生态效益。他们推崇手工劳动，相信手工制 造不仅可降低环境负担，还能加强产品与用户的情感纽带，通 过设计实践传播绿色理念和可持续发展价值"
#     },
#     {
#         "id": 14,
#         "text": "图3:约1975年间，由埃米利奥安巴斯为 Anonima Castelli设计的Vertebra任务椅"
#     },
#     {
#         "id": 15,
#         "text": "激进设计的再次兴起"
#     },
#     {
#         "id": 16,
#         "text": "意大利激进设计在70年代末期重 新嘱起，设计师通过戏仿和实验性 设计挑战主流美学。诸如亚历山德 罗内迪尼的设计将传统家具重新 装饰，利用色彩和图案构建新的文 化符号，这是对现代主义停车设计 的有力回应。"
#     },
#     {
#         "id": 17,
#         "text": "图6:1978年，由亚历山德罗内迪尼为 Studio Alchimia 设计的普鲁斯特扶手椅"
#     },
#     {
#         "id": 18,
#         "text": "图5: 1973年1月的 《Casabella》封面 展示了Global Tools组织的成员"
#     }
# ]

# 按照设计历史的海报主题19世纪90年代的设计历史内容设计的全球化浪潮，进行最贴近主题的分区，不要单纯按出现顺序分组。有的图片跟主题的id顺序不在一起，但你需要根据图片信息和你已知的设计历史的常识，来判断该图片最属于哪个小主题。
# 注意："图片描述"需要与其内容最相关的小主题成为一组。每个图片描述都需要认真思考其与哪个小主题最相关，不要简单地与其前后文本按顺序相关联。图片的顺序有可能与其相隔的内容相关联，请认真考虑。

# # 约束条件 #
# 仅回复所要求的 JSON 输出，遵守上述要求，不包含任何无关信息。
# 请勿在文本中包含参考文献、引文或任何来源注释。!
# 请仅以纯文本形式回复。确保答案不包含任何代码格式或代码块，如 ``json.
# keywords必须是Poster Content中存在的词，不要无中生有，也不要做任何删改。
# 你的输出需要严格按照json格式输出，并考虑到可能的转义字符问题，不要在字符串中再包含英文引号，以防json解析失败。

# '''
# posterContent.add_user_message(content)
# assistantOutput = posterContent.get_reply()
# print(assistantOutput)


# # QwenAssistant 测试
# 创建实例
# assistant_id = 'asst_0c9a8326-2d15-4aa6-96fd-ea4ff9fc87f0'
# workspace = 'llm-8iz1w0zj4paj6z85'
# api_key = 'sk-da762947f89040b0895a6099f807bf62'

# generator_assistant = QwenAssistant(assistant_id, workspace, api_key)

# # 调用方法
# a = generator_assistant.send_message('您好！请问您对后现代主义的哪个方面感兴趣？我们可以探讨其特点、相关运动如孟菲斯运动或新浪潮平面设计，以及它对品牌和国际设计的影响等。')
# print(a)


