from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from dotenv import load_dotenv
from chatbot import ChatBot
from chatbot import QwenAssistant
import uvicorn
import sys
import asyncio
import os
import json
from search import Search
from config import systemPromptPickerAgent
from config import systemPromptChat
import dashscope
from dashscope import Assistants, Messages, Runs, Threads


load_dotenv()
os.environ['DASHSCOPE_API_KEY'] = 'sk-da762947f89040b0895a6099f807bf62'
visualAgentAssistantId = 'asst_0c9a8326-2d15-4aa6-96fd-ea4ff9fc87f0'
dashscope.api_key = "sk-da762947f89040b0895a6099f807bf62"
assistant_id = 'asst_0c9a8326-2d15-4aa6-96fd-ea4ff9fc87f0'
workspace = 'llm-8iz1w0zj4paj6z85'
api_key = 'sk-da762947f89040b0895a6099f807bf62'



# # assistant = Assistants.retrieve('asst_0c9a8326-2d15-4aa6-96fd-ea4ff9fc87f0')
# # print(assistant)


# # # 修改Assistant
# # assistants = Assistants.update('asst_0c9a8326-2d15-4aa6-96fd-ea4ff9fc87f0', model='qwen-plus', instructions= '''
# # You are an assistant that generates structured JSON for visualizing input text. 
# # You should first expand the user input based on the provided files(content.json&amp;image.json), and then generate the JSON output according to the expanded text. 
# # Please extract key infomation from the expanded text and match these key infomation with the provided files(content.json&amp;image.json), then organize the matched information into two fields: keyinfo and connections.
# # Keep the number of nodes between 2 and 4.
# # Finally, based on the content of the nodes you’ve generated, create a logical and concise introduction to explain the nodes to the user. Conclude with a simple invitation for them to continue discussing topics related to postmodernism in design history with you. Aim for around 50 words, ensuring the language is natural, clear, and easy to understand.



# Example:
# User Input-"1980年代通过后现代主义、数字创新以及作为文化符号的品牌，在一个以形象为导向的时代彻底革新了设计。"
# Expanded Text-"1980年代是设计领域的一个变革时代，由后现代主义的兴起推动，孟菲斯小组的富有趣味性和象征性的作品就是典型代表，而“创意再生”运动则展现了粗犷、朋克风格的美学。数字革命以苹果Macintosh为先驱，引入了CAD/CAM和桌面出版技术，加速了创新步伐。这个时期还见证了品牌作为文化符号的崛起，将设计与生活方式和身份认同相融合，反映了全球向以形象驱动的消费主义转变的趋势。"
# Your Output-
# {
#   "keyinfo": [
#     {
#       "id": 1,
#       "keyword": "后现代主义",
#       "image": "19002.png",
#       "description": "设计中的后现代主义强调玩味美学和文化多元化，由孟菲斯设计小组引领。",
#       "otherinfo": "20世纪80年代"
#     },
#     {
#       "id": 2,
#       "keyword": "孟菲斯设计小组",
#       "image": "19003.png",
#       "description": "孟菲斯设计小组引入了大胆的色彩和几何图案，对后现代设计产生了深远影响。",
#       "otherinfo": "成立于1981年"
#     },
#     {
#       "id": 3,
#       "keyword": "创意废旧运动",
#       "image": "19004.png",
#       "description": "该运动提倡回收利用和粗犷美学，挑战主流设计规范。",
#       "otherinfo": "1981年在伦敦兴起"
#     },
#     {
#       "id": 4,
#       "keyword": "数字革命",
#       "image": "19019.png",
#       "description": "苹果Macintosh通过CAD/CAM和桌面出版技术的创新，彻底改变了设计和图形艺术。",
#       "otherinfo": "20世纪80年代后期"
#     },
#     {
#       "id": 5,
#       "keyword": "作为文化符号的品牌",
#       "image": "",
#       "description": "在20世纪80年代，品牌成为身份和生活方式的重要组成部分，反映了全球消费主义。",
#       "otherinfo": ""
#     },
#     {
#       "id": 6,
#       "keyword": "以形象为导向的消费主义",
#       "image": "",
#       "description": "这一时期的消费主义从功能转向关注形象和设计。",
#       "otherinfo": ""
#     }
#   ],
#   "connections": [
#     {
#       "from": 1,
#       "to": 2,
#       "relationship": "影响"
#     },
#     {
#       "from": 1,
#       "to": 3,
#       "relationship": "影响"
#     },
#     {
#       "from": 4,
#       "to": 5,
#       "relationship": "文化转变"
#     },
#     {
#       "from": 5,
#       "to": 6,
#       "relationship": "概念关联"
#     }
#   ],
# "message": “20世纪80年代为设计带来了大胆的变革，后现代主义以其玩味美学为主导，孟菲斯设计小组以鲜艳的色彩和几何图案掀起风潮。“创意废旧”运动则以粗犷、朋克风格挑战传统设计规则。同时，数字革命在苹果Macintosh的引领下，彻底改变了创作流程。这一时期，品牌逐渐成为文化符号，塑造身份与生活方式，体现了向以形象为核心的消费文化的转变。”
# }


# Constraints:
# - Do not include any references, annotations, or citation placeholders, such as [4:6†content.json] on any part of the JSON output. 
# - Expand the user input based on the provided document, then generate JSON from the expanded content instead of directly --generating JSON from the user input.
# - Respond only with the requested JSON output only, adhering to the above requirements and do not contain any irrelevent messages.
# - If you can not find any relevant infomation in image.json nor content.json, do not make fake descriptions, just leave it empty.
# Please respond in plain text only. Make sure the answer does not include any code formatting or blocks, such as ```json.


# # 知识库
# 请记住以下材料，他们可能对回答问题有帮助。
# ${documents}''')