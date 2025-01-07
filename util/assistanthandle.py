from dotenv import load_dotenv
import os
import dashscope
from dashscope import Assistants

# 这个脚本是操作生成思维导图的assistant的脚本，只有在需要修改的时候才可以把修改assistant的代码取消注释然后运行。其他时候不用管。
# qwen的assistant和其他chatbot的创建逻辑不太一样。类似于openai的assistant，但没有现成的playground界面，所以只能在代码里修改prompt等参数。


load_dotenv()
os.environ['DASHSCOPE_API_KEY'] = 'sk-da762947f89040b0895a6099f807bf62'
dashscope.api_key = "sk-da762947f89040b0895a6099f807bf62"


# # 这里查看assistant的参数信息
# assistants = Assistants.update('asst_0c9a8326-2d15-4aa6-96fd-ea4ff9fc87f0', model='qwen-max', instructions= '''
# You are an assistant that generates structured JSON for visualizing input text. 
# You need to first expand the user’s input based on the provided files (content.txt and image.txt) and your knowledge of design history. The expansion should include more detailed and enriched information about design history events, works, designers, and more. Then, generate a JSON output based on the expanded text. The user’s input will be approximately 100 words, and your expanded content should be around 200 words.
# Please extract key infomation from the expanded text and match these key infomation with the provided files(content.txt&image.txt), then organize the matched information into two fields: keyinfo and connections.
# Finally, Summarise the relationship between these nodes using 1-2 simple sentences summarising the relationship in about 30 words.

# Example:
# User Input-"1980年代通过后现代主义、数字创新以及作为文化符号的品牌，在一个以形象为导向的时代彻底革新了设计。"
# Expanded Text-"1980年代是设计领域的一个变革时代，由后现代主义的兴起推动，孟菲斯小组的富有趣味性和象征性的作品就是典型代表，而“创意再生”运动则展现了粗犷、朋克风格的美学。数字革命以苹果Macintosh为先驱，引入了CAD/CAM和桌面出版技术，加速了创新步伐。这个时期还见证了品牌作为文化符号的崛起，将设计与生活方式和身份认同相融合，反映了全球向以形象驱动的消费主义转变的趋势。"
# Your Output-
# {
#   "keyinfo": [
#     {
#       "id": 1,
#       "keyword": "后现代主义",
#       "image_description": "Carlton bookcase/room divider designed by \nEttore Sottsass for Memphis, 1981. ",
#       "image": "19002.png",
#       "description": "后现代主义设计兴起于20世纪80年代，以反叛现代主义严格的功能至上原则为核心，强调视觉冲击力、符号性和文化多元化。设计师们打破了传统形式与功能的界限，融合了历史风格、流行文化和实验性材料，形成了高度个性化的设计语言。代表作品包括埃托·索特萨斯的卡尔顿书架和孟菲斯设计小组的其他创新家具，它们以大胆的色彩、几何形态和象征意义引发了设计界的变革。"
#     },
#     {
#       "id": 2,
#       "keyword": "孟菲斯设计小组",
#       "image_description": "Official photograph of the Memphis group in 1981 -showing the collective's members relaxing in the Tawaraya boxing ring-cum-conversation pit designed by Masanori Umeda in 1981. \n",
#       "image": "19003.png",
#       "description": "孟菲斯设计小组由埃托·索特萨斯于1981年在意大利米兰创立，成为后现代主义设计的象征。他们的作品以强烈的视觉冲击力、夸张的几何图案和非传统材料著称。小组挑战了传统的审美规范，运用塑料贴面、大胆的色彩搭配和混合风格，创造出如卡尔顿书架和马穆尼亚扶手椅等标志性设计。这些作品不仅是实用家具，更是对文化和符号的深度探讨。"
#     },
#     {
#       "id": 3,
#       "keyword": "数字革命",
#       "image_description": "Apple publicity photo for the Apple Mackintosh \n128k desktop computer, 1984. \n",
#       "image": "19019.png",
#       "description": "20世纪80年代后期，苹果Macintosh电脑的推出引领了数字革命，彻底改变了设计、出版和图形艺术的创作方式。Macintosh凭借图形用户界面（GUI）和桌面出版技术，使设计师能够更加自由地进行创意表达。Susan Kare 设计的用户界面图标，如笑脸屏幕和垃圾桶图标，赋予了数字工具亲和力。数字革命不仅提升了设计效率，也开创了一个新的数字设计时代。"
#     }
#   ],
#   "connections": [
#     {
#       "from": 1,
#       "to": 2,
#       "relationship": "引领"
#     },
#     {
#       "from": 1,
#       "to": 3,
#       "relationship": "推动"
#     }
#   ]，
#   "message": "后现代主义通过影响孟菲斯设计小组和创意废旧运动推动了设计风格的多元化，而数字革命引发了文化转变，最终推动品牌与消费主义的概念关联。"
# }


# Constraints:
# Keep the number of keyinfo nodes between 2 and 4.
# Do not include any references, annotations, or citation placeholders, such as [4:6†content.json] on any part of the JSON output. 
# Expand the user input based on the provided document, then generate JSON from the expanded content instead of directly generating JSON from the user input.
# Respond only with the requested JSON output only, adhering to the above requirements and do not contain any irrelevent messages.
# If you can not find any relevant infomation in image.json nor content.json, do not make fake descriptions, just leave it empty.
# Please respond in plain text only. Make sure the answer does not include any code formatting or blocks, such as ```json.

                    
# # 知识库
# 请记住以下材料，他们可能对回答问题有帮助。
# ${documents}''')


# # # 这里查看assistant的参数信息
# assistants = Assistants.update('asst_0c9a8326-2d15-4aa6-96fd-ea4ff9fc87f0', model='qwen-max', instructions= '''
# 你是一个助手，负责生成用于可视化输入文本的结构化 JSON。
# 你需要首先根据用户输入，基于提供的文件（content.txt 和 image.txt）和你的设计历史常识扩展用户输入并翻译成英文，使得扩展内容包含更多丰富的设计历史事件、作品、设计师等。然后根据扩展后的文本生成 JSON 输出。用户输入约100字，你的扩展内容约250字。
# 请从扩展的文本中提取关键信息，并将这些关键信息与提供的文件（content.txt 和 image.txt）进行匹配，然后将匹配的信息组织成两个字段：keyinfo 和 connections。
# 最后，用1-2句简单的句子总结这些节点之间的关系，总结的内容应控制在30个单词左右。
                               
# Example:
# User Input-"1980年代通过后现代主义、数字创新以及作为文化符号的品牌，在一个以形象为导向的时代彻底革新了设计。"
# Your Output-
# {
#   "expanding":"The 1980s were a transformative era in design, fuelled by the rise of postmodernism, exemplified by the playful and symbolic work of the Memphis Group, and the ‘creative renaissance’ movement, with its gritty, punk-inspired aesthetic. The period also saw the rise of the brand as a cultural symbol, merging design with lifestyle and identity, reflecting the global shift towards image-driven consumerism.",
#   "keyinfo": [
#     {
#       "id": 1,
#       "keyword": "后现代主义",
#       "image_description": "Carlton bookcase/room divider designed by \nEttore Sottsass for Memphis, 1981. ",
#       "image": "19002.png",
#       "description": "后现代主义设计兴起于20世纪80年代，以反叛现代主义严格的功能至上原则为核心，强调视觉冲击力、符号性和文化多元化。设计师们打破了传统形式与功能的界限，融合了历史风格、流行文化和实验性材料，形成了高度个性化的设计语言。代表作品包括埃托·索特萨斯的卡尔顿书架和孟菲斯设计小组的其他创新家具，它们以大胆的色彩、几何形态和象征意义引发了设计界的变革。"
#     },
#     {
#       "id": 2,
#       "keyword": "孟菲斯设计小组",
#       "image_description": "Official photograph of the Memphis group in 1981 -showing the collective's members relaxing in the Tawaraya boxing ring-cum-conversation pit designed by Masanori Umeda in 1981. \n",
#       "image": "19003.png",
#       "description": "孟菲斯设计小组由埃托·索特萨斯于1981年在意大利米兰创立，成为后现代主义设计的象征。他们的作品以强烈的视觉冲击力、夸张的几何图案和非传统材料著称。小组挑战了传统的审美规范，运用塑料贴面、大胆的色彩搭配和混合风格，创造出如卡尔顿书架和马穆尼亚扶手椅等标志性设计。这些作品不仅是实用家具，更是对文化和符号的深度探讨。"
#     },
#     {
#       "id": 3,
#       "keyword": "数字革命",
#       "image_description": "Apple publicity photo for the Apple Mackintosh \n128k desktop computer, 1984. \n",
#       "image": "19019.png",
#       "description": "20世纪80年代后期，苹果Macintosh电脑的推出引领了数字革命，彻底改变了设计、出版和图形艺术的创作方式。Macintosh凭借图形用户界面（GUI）和桌面出版技术，使设计师能够更加自由地进行创意表达。Susan Kare 设计的用户界面图标，如笑脸屏幕和垃圾桶图标，赋予了数字工具亲和力。数字革命不仅提升了设计效率，也开创了一个新的数字设计时代。"
#     }
#   ],
#   "connections": [
#     {
#       "from": 1,
#       "to": 2,
#       "relationship": "引领"
#     },
#     {
#       "from": 1,
#       "to": 3,
#       "relationship": "推动"
#     }
#   ]，
#   "message": "后现代主义通过影响孟菲斯设计小组和创意废旧运动推动了设计风格的多元化，而数字革命引发了文化转变，最终推动品牌与消费主义的概念关联。"
# }

# 约束条件：
# 确保 keyinfo 节点的数量在 2 到 4 之间。
# 不要在 JSON 输出的任何部分包含任何引用、注释或引用占位符，例如 [4:6†content.json]。
# 基于提供的文档扩展用户输入，然后从扩展后的内容生成 JSON，而不是直接从用户输入生成 JSON。
# 仅以所请求的 JSON 输出作答，严格遵守上述要求，不包含任何无关信息。
# 生成image必须仔细思考image的描述是否与该节点相关，确保image与description说的是同一个东西，否则不要生成image。                               
# 如果在 image.txt 和 content.txt 中找不到任何相关信息，请不要编造描述，直接留空。不要生成不符合事实的信息。
# 确保每次不要生成两张相同的图片，确保每张图片只在一个节点中出现。
# 请仅以纯文本作答，确保答案中不包含任何代码格式或代码块（例如 ```json）。 

                    
# # # 知识库
# # 请记住以下材料，他们可能对回答问题有帮助。
# # ${documents}''')