from config import systemPromptPickerAgent1, systemPromptPickerAgent2, systemPromptPickerAgent3
from chatbot import ChatBot
import json


# def Search(assistant_output: str, json_database_path: str):
#     # 将字符串解析为 JSON
#     assistant_data = json.loads(assistant_output)
#     description = assistant_data["Dialogue"]
#     highlighted = assistant_data["highlighted"]
#     emotion = assistant_data["ConversationStyle"]  # 直接获取字符串格式的 ConversationStyle

#     # 初始化输出数据
#     output = [description]  # result[0]
#     titles = []             # 存储所有小主题和海报标题 bbox，调整为列表形式 result[1]
#     keywords = []           # 存储所有关键词的 bbox result[2]
#     captions = []           # 存储所有图片描述的 bbox，调整为列表形式 result[3]

#     # 加载数据库
#     with open(json_database_path, 'r', encoding='utf-8') as f:
#         database = json.load(f)

#     # 遍历 highlighted 部分
#     for item in highlighted:
#         group_id = str(item["id"])  # 转为字符串以匹配 JSON 数据
#         highlight_type = item["type"]
#         keywords_list = item.get("keywords", [])

#         # 查找 group_id 对应的数据
#         group_data = next((data for data in database if str(data["group_id"]) == group_id), None)
#         if not group_data:
#             print(f"Group ID {group_id} not found.")
#             continue

#         # 根据类型分类
#         if highlight_type in ["小主题", "海报标题"]:
#             # 小主题和海报标题
#             titles.append(group_data["bbox"])

#         elif highlight_type == "文本内容":
#             # 关键词匹配
#             matched_bboxes = []
#             all_words = []  # 用于存储所有行的 words 数据
#             for line in group_data.get("lines", []):
#                 all_words.extend(line.get("words", []))  # 聚合所有行的 words

#             # 遍历关键词
#             for keyword in keywords_list:
#                 keyword_bboxes = []
#                 keyword_length = len(keyword)
#                 temp_match = []  # 暂存当前匹配的 bbox
#                 word_index = 0

#                 # 遍历所有 words，查找匹配关键词
#                 while word_index < len(all_words):
#                     word_data = all_words[word_index]
#                     word_text = word_data.get("word", "").strip()

#                     if not word_text:  # 跳过空格
#                         word_index += 1
#                         continue

#                     # 匹配当前关键词的第一个字符
#                     if word_text == keyword[len(temp_match)]:
#                         temp_match.append(word_data["bbox"])
#                         if len(temp_match) == keyword_length:  # 完成一个关键词匹配
#                             keyword_bboxes.extend(temp_match)
#                             temp_match = []  # 重置临时匹配
#                     else:
#                         temp_match = []  # 重置匹配状态

#                     word_index += 1

#                 # 如果找到关键词的 bbox，添加到结果中
#                 if keyword_bboxes:
#                     matched_bboxes.extend(keyword_bboxes)

#             # 添加匹配到的关键词 bbox 数据
#             keywords.append(matched_bboxes)

#         elif highlight_type == "图片描述":
#             # 图片描述
#             captions.append(group_data["bbox"])

#     # 整理结果
#     output.append(titles)     # result[1]: 小主题/海报标题，列表形式
#     output.append(keywords)   # result[2]: 关键词的 bbox
#     output.append(captions)   # result[3]: 图片描述，列表形式
#     output.append(emotion)    # result[4]: Emotion
#     return output

import re

def preprocess_json(json_string):
    """
    预处理 JSON 字符串，修复常见格式问题，包括去除 ```json 和 ``` 标记。
    """
    # 移除 ```json 和 ``` 的标记
    if json_string.startswith("```json"):
        json_string = json_string[7:].strip()  # 移除开头的 ```json
    if json_string.endswith("```"):
        json_string = json_string[:-3].strip()  # 移除结尾的 ```

    try:
        # 尝试直接解析 JSON 字符串
        return json.loads(json_string)
    except json.JSONDecodeError:
        # 修复 JSON 中的无引号键和值
        json_string = re.sub(r'(?<!")(\b\w+\b)(?=\s*:)', r'"\1"', json_string)  # 为键补充引号
        json_string = re.sub(r':\s*(\b\w+\b)(?=\s*[,\}])', r': "\1"', json_string)  # 为值补充引号
        # 再次尝试解析修复后的字符串
        try:
            return json.loads(json_string)
        except json.JSONDecodeError:
            # 如果仍然无法解析，返回一个默认的空结构
            return {
                "highlighted": [],
                "ConversationStyle": "",
                "Dialogue": ""
            }

def fill_defaults(assistant_data):
    """
    为空字段填充默认值
    """
    if not assistant_data.get("highlighted"):
        assistant_data["highlighted"] = []
    if not assistant_data.get("ConversationStyle"):
        assistant_data["ConversationStyle"] = "Unknown"
    if not assistant_data.get("Dialogue"):
        assistant_data["Dialogue"] = "对不起对不起对不起，我刚刚走神了，你可以重复一遍你的问题吗？"
    return assistant_data

def Search(assistant_output: str, json_database_path: str):
    # 预处理 JSON 数据
    assistant_data = preprocess_json(assistant_output)
    
    # 填充默认值
    assistant_data = fill_defaults(assistant_data)

    # 提取必要字段
    description = assistant_data["Dialogue"]
    highlighted = assistant_data["highlighted"]
    emotion = assistant_data["ConversationStyle"]

    # 初始化输出数据
    output = [description]  # result[0]
    titles = []             # 存储所有小主题和海报标题 bbox，调整为列表形式 result[1]
    keywords = []           # 存储所有关键词的 bbox result[2]
    captions = []           # 存储所有图片描述的 bbox，调整为列表形式 result[3]

    # 加载数据库
    try:
        with open(json_database_path, 'r', encoding='utf-8') as f:
            database = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        print(f"Error: Could not load database from {json_database_path}.")
        return []

    # 遍历 highlighted 部分
    for item in highlighted:
        group_id = str(item.get("id", ""))  # 转为字符串以匹配 JSON 数据
        highlight_type = item.get("type", "")
        keywords_list = item.get("keywords", [])

        # 查找 group_id 对应的数据
        group_data = next((data for data in database if str(data.get("group_id", "")) == group_id), None)
        if not group_data:
            print(f"Group ID {group_id} not found.")
            continue

        # 根据类型分类
        if highlight_type in ["小主题", "海报标题"]:
            # 小主题和海报标题
            titles.append(group_data.get("bbox", {}))

        elif highlight_type == "文本内容":
            # 关键词匹配
            matched_bboxes = []
            all_words = []  # 用于存储所有行的 words 数据
            for line in group_data.get("lines", []):
                all_words.extend(line.get("words", []))  # 聚合所有行的 words

            # 遍历关键词
            for keyword in keywords_list:
                keyword_bboxes = []
                keyword_length = len(keyword)
                temp_match = []  # 暂存当前匹配的 bbox
                word_index = 0

                # 遍历所有 words，查找匹配关键词
                while word_index < len(all_words):
                    word_data = all_words[word_index]
                    word_text = word_data.get("word", "").strip()

                    if not word_text:  # 跳过空格
                        word_index += 1
                        continue

                    # 匹配当前关键词的第一个字符
                    if word_text == keyword[len(temp_match)]:
                        temp_match.append(word_data.get("bbox", {}))
                        if len(temp_match) == keyword_length:  # 完成一个关键词匹配
                            keyword_bboxes.extend(temp_match)
                            temp_match = []  # 重置临时匹配
                    else:
                        temp_match = []  # 重置匹配状态

                    word_index += 1

                # 如果找到关键词的 bbox，添加到结果中
                if keyword_bboxes:
                    matched_bboxes.extend(keyword_bboxes)

            # 添加匹配到的关键词 bbox 数据
            keywords.append(matched_bboxes)

        elif highlight_type == "图片描述":
            # 图片描述
            captions.append(group_data.get("bbox", {}))

    # 整理结果
    output.append(titles)     # result[1]: 小主题/海报标题，列表形式
    output.append(keywords)   # result[2]: 关键词的 bbox
    output.append(captions)   # result[3]: 图片描述，列表形式
    output.append(emotion)    # result[4]: ConversationType
    return output

# posterTalker = ChatBot(systemPrompt=systemPromptPickerAgent2, model="qwen-turbo")  
# content = """
# 介绍品牌崛起和孟菲斯运动。
# 仅回复所要求的 JSON 输出，遵守上述要求，不包含任何无关信息。
# 请勿在文本中包含参考文献、引文或任何来源注释。!
# 请仅以纯文本形式回复。确保答案不包含任何代码格式或代码块，如 ``json.
# """
# posterTalker.add_user_message(content)
# assistantOutput = posterTalker.get_reply()
# print(assistantOutput)

# output = Search(assistantOutput, 'eval2_grouped.json')
# print(output)