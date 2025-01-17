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

# def preprocess_json(json_string):
#     """
#     预处理 JSON 字符串，修复常见格式问题，包括去除 ```json 和 ``` 标记。
#     """
#     # 移除 ```json 和 ``` 的标记
#     if json_string.startswith("```json"):
#         json_string = json_string[7:].strip()  # 移除开头的 ```json
#     if json_string.endswith("```"):
#         json_string = json_string[:-3].strip()  # 移除结尾的 ```

#     try:
#         # 尝试直接解析 JSON 字符串
#         return json.loads(json_string)
#     except json.JSONDecodeError:
#         # 修复 JSON 中的无引号键和值
#         json_string = re.sub(r'(?<!")(\b\w+\b)(?=\s*:)', r'"\1"', json_string)  # 为键补充引号
#         json_string = re.sub(r':\s*(\b\w+\b)(?=\s*[,\}])', r': "\1"', json_string)  # 为值补充引号
#         # 再次尝试解析修复后的字符串
#         try:
#             return json.loads(json_string)
#         except json.JSONDecodeError:
#             # 如果仍然无法解析，返回一个默认的空结构
#             return {
#                 "highlighted": [],
#                 "ConversationStyle": "",
#                 "Dialogue": ""
#             }

# def fill_defaults(assistant_data):
#     """
#     为空字段填充默认值
#     """
#     if not assistant_data.get("highlighted"):
#         assistant_data["highlighted"] = []
#     if not assistant_data.get("ConversationStyle"):
#         assistant_data["ConversationStyle"] = "Unknown"
#     if not assistant_data.get("Dialogue"):
#         assistant_data["Dialogue"] = "对不起对不起对不起，我刚刚走神了，你可以重复一遍你的问题吗？"
#     return assistant_data

# def Search(assistant_output: str, json_database_path: str):
#     # 预处理 JSON 数据
#     assistant_data = preprocess_json(assistant_output)
    
#     # 填充默认值
#     assistant_data = fill_defaults(assistant_data)

#     # 提取必要字段
#     description = assistant_data["Dialogue"]
#     highlighted = assistant_data["highlighted"]
#     emotion = assistant_data["ConversationStyle"]

#     # 初始化输出数据
#     output = [description]  # result[0]
#     titles = []             # 存储所有小主题和海报标题 bbox，调整为列表形式 result[1]
#     keywords = []           # 存储所有关键词的 bbox result[2]
#     captions = []           # 存储所有图片描述的 bbox，调整为列表形式 result[3]

#     # 加载数据库
#     try:
#         with open(json_database_path, 'r', encoding='utf-8') as f:
#             database = json.load(f)
#     except (FileNotFoundError, json.JSONDecodeError):
#         print(f"Error: Could not load database from {json_database_path}.")
#         return []

#     # 遍历 highlighted 部分
#     for item in highlighted:
#         group_id = str(item.get("id", ""))  # 转为字符串以匹配 JSON 数据
#         highlight_type = item.get("type", "")
#         keywords_list = item.get("keywords", [])

#         # 查找 group_id 对应的数据
#         group_data = next((data for data in database if str(data.get("group_id", "")) == group_id), None)
#         if not group_data:
#             print(f"Group ID {group_id} not found.")
#             continue

#         # 根据类型分类
#         if highlight_type in ["小主题", "海报标题"]:
#             # 小主题和海报标题
#             titles.append(group_data.get("bbox", {}))

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
#                         temp_match.append(word_data.get("bbox", {}))
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
#             captions.append(group_data.get("bbox", {}))

#     # 整理结果
#     output.append(titles)     # result[1]: 小主题/海报标题，列表形式
#     output.append(keywords)   # result[2]: 关键词的 bbox
#     output.append(captions)   # result[3]: 图片描述，列表形式
#     output.append(emotion)    # result[4]: ConversationType
#     return output



import json
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
    """
    根据 assistant_output 中的 highlight 内容，去数据库里找到对应的 bbox 信息。
    - output[0] : 对话文本
    - output[1] : 小主题/海报标题 bbox 列表
    - output[2] : 关键词（文本内容）的 bbox 列表（可能包含多组匹配结果）
    - output[3] : 图片描述 bbox 列表
    - output[4] : 会话风格/情绪（ConversationStyle）
    """
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
    titles = []             # result[1]
    keywords = []           # result[2]
    captions = []           # result[3]

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

        # 在数据库中查找对应 group_id 的数据
        group_data = next((data for data in database if str(data.get("group_id", "")) == group_id), None)
        if not group_data:
            print(f"Group ID {group_id} not found.")
            continue

        # 根据类型分类
        if highlight_type in ["小主题", "海报标题"]:
            # 小主题和海报标题
            titles.append(group_data.get("bbox", {}))

        elif highlight_type == "文本内容":
            # ========== 多词组/短语匹配逻辑 ==========

            # 先把每一行的 words 全都收集到 all_words 列表中
            all_words = []
            for line in group_data.get("lines", []):
                all_words.extend(line.get("words", []))  # 每个 word 包含 { "word": "XXX", "bbox": [...] }

            matched_bboxes = []  # 总的匹配结果

            # 针对每一个 keyword（可能是单词或多单词短语）
            for keyword in keywords_list:
                # 将关键字按空格拆分，如 "steel beams" -> ["steel", "beams"]
                split_keyword = keyword.strip().split()
                n = len(split_keyword)
                if n == 0:
                    continue

                # 在 all_words 中用滑窗法匹配
                # 每个位置尝试匹配下 n 个连续单词
                i = 0
                while i <= len(all_words) - n:
                    match = True
                    for j in range(n):
                        # 取出 OCR 里的实际 word 文本，去掉首尾空格，然后忽略大小写
                        ocr_word = all_words[i + j].get("word", "").strip().lower()
                        if ocr_word != split_keyword[j].lower():
                            match = False
                            break
                    if match:
                        # 如果完全匹配，就把这 n 个单词的 bbox 都纳入 matched_bboxes
                        for j in range(n):
                            matched_bboxes.append(all_words[i + j].get("bbox", {}))
                        # 匹配到之后，如果你想允许关键词在文本中重叠，可以只让 i += 1 
                        # 如果你想避免重叠的情况，可以 i += n
                        i += n
                    else:
                        i += 1

            # 最后将匹配到的 bbox 添加到 keywords
            keywords.append(matched_bboxes)

        elif highlight_type == "图片描述":
            # 图片描述
            captions.append(group_data.get("bbox", {}))

    # 整理结果
    output.append(titles)     # result[1]: 小主题/海报标题
    output.append(keywords)   # result[2]: 关键词 bbox
    output.append(captions)   # result[3]: 图片描述
    output.append(emotion)    # result[4]: ConversationStyle
    return output


posterTalker = ChatBot(systemPrompt=systemPromptPickerAgent1, model="qwen-turbo")  
content = """
please introduce the high-tech style
"""
posterTalker.add_user_message(content)
assistantOutput = posterTalker.get_reply()
print(assistantOutput)

output = Search(assistantOutput, 'eval1_grouped.json')
print(output)