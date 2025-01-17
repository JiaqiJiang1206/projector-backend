from openai import OpenAI
from config import systemPromptSemanticAgent
from config import systemPromptPickerAgent1, systemPromptPickerAgent2, systemPromptPickerAgent3
import os
from dotenv import load_dotenv
from dashscope import Assistants, Messages, Runs, Threads
import dashscope

# 加载环境变量
load_dotenv()
apiKey = "sk-da762947f89040b0895a6099f807bf62"
assistant_id = 'asst_0c9a8326-2d15-4aa6-96fd-ea4ff9fc87f0'
api_key = "sk-da762947f89040b0895a6099f807bf62"
dashscope.api_key = api_key

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

# client = OpenAI()

# def get_ai_reply(user_message):
#     """
#     与 OpenAI Assistant 交互并获取回复的函数。
    
#     参数:
#         user_message (str): 用户发送的消息。
    
#     返回:
#         dict: 包含 AI 回复的解析数据。
#     """
#     try:
#         # 从 Playground 中调用助手
#         assistant = client.beta.assistants.retrieve("asst_YpyxHD5eDY3bmbUqJhDSV0Ij")

#         # 创建线程
#         thread = client.beta.threads.create()

#         # 向线程发送用户消息
#         client.beta.threads.messages.create(
#             thread_id=thread.id,
#             role="user",
#             content=user_message
#         )

#         # 启动并轮询运行
#         run = client.beta.threads.runs.create_and_poll(
#             thread_id=thread.id,
#             assistant_id=assistant.id,
#             instructions=""
#         )

#         if run.status == 'completed':
#             # 获取线程消息
#             messages = client.beta.threads.messages.list(thread_id=thread.id)

#             # 提取 AI 回复
#             for message in messages.data:
#                 if message.role == 'assistant':  # 只提取 AI 回复
#                     raw_reply = message.content[0].text.value  # 获取文本内容
#                     return raw_reply  # 返回解析后的数据
#         else:
#             return {"error": f"AI 运行未完成，状态: {run.status}"}

#     except Exception as e:
#         # 捕获并返回任何错误
#         return {"error": str(e)}

class Assistantbot:
    def __init__(self, client, assistant_id):
        """
        初始化与 OpenAI Assistant 的交互。

        参数:
            client (object): 用于与 OpenAI API 进行交互的客户端。
            assistant_id (str): OpenAI Assistant 的 ID。
        """
        self.client = client
        self.assistant_id = assistant_id

    def get_ai_reply(self, user_message):
        """
        与 OpenAI Assistant 交互并获取回复。

        参数:
            user_message (str): 用户发送的消息。

        返回:
            dict: 包含 AI 回复的解析数据。
        """
        try:
            # 从 Playground 中调用助手
            assistant = self.client.beta.assistants.retrieve(self.assistant_id)

            # 创建线程
            thread = self.client.beta.threads.create()

            # 向线程发送用户消息
            self.client.beta.threads.messages.create(
                thread_id=thread.id,
                role="user",
                content=user_message
            )

            # 启动并轮询运行
            run = self.client.beta.threads.runs.create_and_poll(
                thread_id=thread.id,
                assistant_id=assistant.id,
                instructions=""
            )

            if run.status == 'completed':
                # 获取线程消息
                messages = self.client.beta.threads.messages.list(thread_id=thread.id)

                # 提取 AI 回复
                for message in messages.data:
                    if message.role == 'assistant':  # 只提取 AI 回复
                        raw_reply = message.content[0].text.value  # 获取文本内容
                        return raw_reply  
            else:
                return {"error": f"AI 运行未完成，状态: {run.status}"}

        except Exception as e:
            # 捕获并返回任何错误
            return {"error": str(e)}



# test
# client = OpenAI()
# GeneratorAssistant = Assistantbot(client, "asst_YpyxHD5eDY3bmbUqJhDSV0Ij")
# reply = GeneratorAssistant.get_ai_reply("荷兰设计至今依然保持着其独特的风格和创新精神。除了Droog和Moooi，还有很多其他设计师和品牌在国际上享有盛誉。例如，Studio Job的作品以其大胆的色彩和复杂的图案闻名，而Marcel Wanders则以其浪漫和戏剧性的设计著称。这些设计师的作品继续在全球范围内产生影响。")
# print(reply)

# systemPromptPickerAgent 测试
posterContent = ChatBot(systemPrompt=systemPromptSemanticAgent, model="qwen-max-2024-09-19")
content = '''
按照设计历史的海报主题，进行最贴近主题的分区，不要单纯按出现顺序分组。有的图片跟主题的id顺序不在一起，但你需要根据图片信息和你已知的设计历史的常识，来判断该图片最属于哪个小主题。

海报内容：
[
    {
        "id": 0,
        "text": "The Globalization Wave of Design"
    },
    {
        "id": 1,
        "text": "The Rise of ClobalDesignlcons"
    },
    {
        "id": 2,
        "text": "Apple's Influence and Intelligent Design"
    },
    {
        "id": 3,
        "text": "The fall of theBerlin Wall in1989 marked the beginning of a new international order, and the design world witnessed the rise of global design icons during this period. Designers such as Ronan Arad and Jasper Morrison emerged gaining extensive media exposure and worldwide recognition. Their creative works highlighted the global and diverse nature of design, making it an essential medium"
    },
    {
        "id": 4,
        "text": "Under Jonathan Ive's leadership, Apple redefined intelligent design with products like the iMac and iPhone. These products won users' favor through intuitive interfaces and innovative features, symbolizing the perfect marriage of design and technology. Through intelligent design, Apple made its products an integral part of persona life, inspiring tech companies to explore the possibilities of design innovation."
    },
    {
        "id": 5,
        "text": "cross-border exchange."
    },
    {
        "id": 6,
        "text": "Figure 1: The Bookworm boakshelf designed by Ronan Arad for Kartellin 1994"
    },
    {
        "id": 7,
        "text": "Figure 2: The iMac personal computer designed by Jonathan Ive and the Apple design team in 1998"
    },
    {
        "id": 8,
        "text": "The Impact of Cross-CulturalDesign"
    },
    {
        "id": 9,
        "text": "The Integration of Art and Design"
    },
    {
        "id": 10,
        "text": "Cross-cultural design has flourished in the context of globalization, as designers incorporate elements from diverse cultures to create global producis. For example, Philippe Starck combined Easternminimalist aesthetics with Western design to produce uniquely captivating works. This cultural blending not only enriched the diversity of design but also allowed consumers in qlobal markets to experience the charm of multiculturalism, promoting desian innovation and international exchange"
    },
    {
        "id": 11,
        "text": "As design evolved, the concept of design art continued to expand and deepen. The integration of art and design was not limited to aestheticappeal but also achieved innovation in functionality and form,becoming an important trend in modern design. The Algue Screen System exemplifies this by combining organic forms with modular compositions, perfectly merging art and utility. It not only delivers a visually artistic experience but also demonstrates modern design's pursuit of balancing cultural values and functional needs"
    },
    {
        "id": 12,
        "text": "New Dutch Design"
    },
    {
        "id": 13,
        "text": "Dutch design has gained international prominence, with Droog and Moooi as key representatives. Their designs, characterized by unique humor and minimalist style, broke traditional design boundaries. Dutch design groups focused on innovative materials and distinctive design languages, creating a visual revolution that established Dutch design asa significant force AAAA in the qlobal design scene."
    },
    {
        "id": 14,
        "text": "Figure 3: The Smoke series furniture designed by Maarten Baas for Moooiin 2002"
    },
    {
        "id": 15,
        "text": "Sustainable Design Approaches"
    },
    {
        "id": 16,
        "text": "A new generation of designers focuses on sustainability emphasizing waste reduction during production and advocating for the use of recyclable materials and technologies to maximize environmental benefits. This approach to sustainable design is not only a responsibility toward the environment but also a direction for future design becoming an integral part of harmonious social development."
    },
    {
        "id": 17,
        "text": "Figure 4:The Algue Screen System designed by Ronan and Erwan Bouroullec forVitrain 2004"
    }
]

按照设计历史的海报主题，进行最贴近主题的分区，不要单纯按出现顺序分组。有的图片跟主题的id顺序不在一起，但你需要根据图片信息和你已知的设计历史的常识，来判断该图片最属于哪个小主题。
注意："图片描述"需要与其内容最相关的小主题成为一组。每个图片描述都需要认真思考其与哪个小主题最相关，不要简单地与其前后文本按顺序相关联。图片的顺序有可能与其相隔的内容相关联，请认真考虑。

# 约束条件 #
仅回复所要求的 JSON 输出，遵守上述要求，不包含任何无关信息。
请勿在文本中包含参考文献、引文或任何来源注释。!
请仅以纯文本形式回复。确保答案不包含任何代码格式或代码块，如 ``json.
keywords必须是Poster Content中存在的词，不要无中生有，也不要做任何删改。
你的输出需要严格按照json格式输出，并考虑到可能的转义字符问题，不要在字符串中再包含英文引号，以防json解析失败。

'''
posterContent.add_user_message(content)
assistantOutput = posterContent.get_reply()
print(assistantOutput)


# # QwenAssistant 测试
# 创建实例
# assistant_id = 'asst_0c9a8326-2d15-4aa6-96fd-ea4ff9fc87f0'
# workspace = 'llm-8iz1w0zj4paj6z85'
# api_key = 'sk-da762947f89040b0895a6099f807bf62'

# generator_assistant = QwenAssistant(assistant_id, workspace, api_key)

# # 调用方法
# a = generator_assistant.send_message("""Dutch design still maintains its unique style and innovative spirit today. In addition to Droog and Moooi, there are many other designers and brands with international reputations. Studio Job, for example, is known for its bold colours and intricate patterns, while Marcel Wanders is known for his romantic and dramatic designs. The work of these designers continues to make an impact on a global scale.
                                     
#                                      """)
# print(a)


# # PickerAgent 测试
# PickerAgent1 = ChatBot(systemPromptPickerAgent3, model="qwen-turbo-latest",)
# content = '''乔纳森艾夫和乔布斯是同一个时期的人吗？'''
# PickerAgent1.add_user_message(content)
# reply = PickerAgent1.get_reply()
# print(reply)