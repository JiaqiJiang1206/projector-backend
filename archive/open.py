# from openai import OpenAI
# import os
# from dotenv import load_dotenv

# # 加载 .env 文件中的环境变量
# load_dotenv()

# client = OpenAI()

# #从playground中调用assistant
# assistant = client.beta.assistants.retrieve("asst_YpyxHD5eDY3bmbUqJhDSV0Ij")

# thread = client.beta.threads.create()

# message = client.beta.threads.messages.create(
# thread_id=thread.id,
# role="user",
# content="荷兰设计至今依然保持着其独特的风格和创新精神。除了Droog和Moooi，还有很多其他设计师和品牌在国际上享有盛誉。例如，Studio Job的作品以其大胆的色彩和复杂的图案闻名，而Marcel Wanders则以其浪漫和戏剧性的设计著称。这些设计师的作品继续在全球范围内产生影响。"
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


# # 提取 AI 回复的内容
# for message in messages.data:
#     if message.role == 'assistant':
#         assistant_reply = message.content[0].text.value  # 获取文本内容
#         break

# # 打印 AI 回复
# print(assistant_reply)




