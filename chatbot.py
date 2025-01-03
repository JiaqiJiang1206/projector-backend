from openai import OpenAI
from config import systemPromptSemanticAgent
# from config import systemPromptPickerAgent
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
posterContent = ChatBot(systemPrompt=systemPromptSemanticAgent, model="qwen-max-2024-09-19")
content = '''
按照设计历史的海报主题19世纪90年代的设计历史内容设计的全球化浪潮，进行最贴近主题的分区，不要单纯按出现顺序分组。有的图片跟主题的id顺序不在一起，但你需要根据图片信息和你已知的设计历史的常识，来判断该图片最属于哪个小主题。

[
    {
        "id": 0,
        "text": "设计的全球化浪潮"
    },
    {
        "id": 1,
        "text": "全球设计明星的嘱起"
    },
    {
        "id": 2,
        "text": "苹果的影响力与智能设计"
    },
    {
        "id": 3,
        "text": "苹果公司在乔纳森艾夫的带领下，以iMac和 iPhone等产品重新定义智能设计。这些产品凭直 观界面和创新功能赢得用户喜爱，同时标志着设 计与技术的完美结合。苹果通过智能设计，让产 品成为个人生活的重要部分，激励科技公司探索 设计创新的可能性。"
    },
    {
        "id": 4,
        "text": "1989年柏林墙倒塌象征着新国际秩序的开端 设计界也在此时见证了全球设计明星的崛起，如 罗南阿拉德和贾斯珀莫里森等设计师涌现，他 们的作品吸引了大量媒体曝光并赢得世界范围认 可。这些设计师通过创造性作品强调设计的全球 性和多样化，使其成为跨国交流的重要载体。"
    },
    {
        "id": 5,
        "text": "图1:1994年，由罗南阿拉德为Kartell设计的Bookworm书架"
    },
    {
        "id": 6,
        "text": "图2:1998年由乔纳森艾夫和苹果设计团队设计的iMac个人电脑"
    },
    {
        "id": 7,
        "text": "艺术与设计的结合"
    },
    {
        "id": 8,
        "text": "跨文化设计的影响"
    },
    {
        "id": 9,
        "text": "跨文化设计在全球化背景下日益兴盛，设计师通过融合不同文化的元 素创作出全球化产品。例如，Philippe Starck将东方简约美学结合西 方设计，创造出独具魅力的产品。这种文化交融不仅丰富了设计的多 样性，还让消费者在全球市场中体验多元文化的魅力，促进了设计的 创新与全球交流。"
    },
    {
        "id": 10,
        "text": "在设计发展的同时，设计艺术的概念也 在不断扩展和深化，艺术与设计的融合 不仅体现在视觉的美观上，更是在功能 与形式上实现创新，成为现代设计的重 要趋势。以 Alque屏风系统为例，该作 品以有机形态和模块化组合将艺术与实 用完美结合，不仅带来富有装艺术感 的视觉体验，也彰显了现代设计对文化 价值与功能需求的平衡追求。"
    },
    {
        "id": 11,
        "text": "新荷兰设计"
    },
    {
        "id": 12,
        "text": "荷兰设计在国际上的崭露头角，Droog和Moooi是其代表。它们的 设计作品以独特的幽默感和简约风格，打破了传统设计的界限。荷 兰设计团体注重使用创新的材料和独特的设计语言，带来了一场视 AAAAA 觉上的革命，使得荷兰设计在全球设计界占据了一席之地。"
    },
    {
        "id": 13,
        "text": "图3:2002年，马滕巴斯为Moooi设计的Smoke系列家"
    },
    {
        "id": 14,
        "text": "可持续发展的设计思路"
    },
    {
        "id": 15,
        "text": "新一代设计师慈加关注可持续发展。设计师们通过减少生产中的浪 费，推崇使用可循环的材料和技术，以实现环境效益的最大化。 这种可持续设计思路不仅是对环境的责任，也引领了未来设计的方 向，成为社会和谐发展的重要组成部分。"
    },
    {
        "id": 16,
        "text": "图4:2004年，由罗南和埃尔万布鲁莱克为Vitra 设计的Algue屏风系统。"
    }
]

按照设计历史的海报主题19世纪90年代的设计历史内容设计的全球化浪潮，进行最贴近主题的分区，不要单纯按出现顺序分组。有的图片跟主题的id顺序不在一起，但你需要根据图片信息和你已知的设计历史的常识，来判断该图片最属于哪个小主题。
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
# a = generator_assistant.send_message('您好！请问您对后现代主义的哪个方面感兴趣？我们可以探讨其特点、相关运动如孟菲斯运动或新浪潮平面设计，以及它对品牌和国际设计的影响等。')
# print(a)


