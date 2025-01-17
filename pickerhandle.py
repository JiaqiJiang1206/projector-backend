from config import systemPromptPickerAgent1, systemPromptPickerAgent2, systemPromptPickerAgent3
from chatbot import ChatBot
import json
import json
import re
from difflib import SequenceMatcher

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
# import json
# from fuzzywuzzy import fuzz

# def preprocess_json(json_string):
#     """
#     Preprocess the JSON string to fix common format issues.
#     """
#     if json_string.startswith("```json"):
#         json_string = json_string[7:].strip()
#     if json_string.endswith("```"):
#         json_string = json_string[:-3].strip()

#     try:
#         return json.loads(json_string)
#     except json.JSONDecodeError:
#         # Attempt to fix unquoted keys and values
#         json_string = re.sub(r'(?<!")\b\w+\b(?=\s*:)','"\\g<0>"', json_string)
#         json_string = re.sub(r':\s*(\b\w+\b)', r': "\\g<1>"', json_string)
#         try:
#             return json.loads(json_string)
#         except json.JSONDecodeError:
#             return {"highlighted": [], "ConversationStyle": "", "Dialogue": ""}

# def fill_defaults(assistant_data):
#     """
#     Fill in default values for missing fields in the assistant data.
#     """
#     if not assistant_data.get("highlighted"):
#         assistant_data["highlighted"] = []
#     if not assistant_data.get("ConversationStyle"):
#         assistant_data["ConversationStyle"] = "Unknown"
#     if not assistant_data.get("Dialogue"):
#         assistant_data["Dialogue"] = "Please clarify your question."
#     return assistant_data

# def find_keyword_positions(keywords, all_words):
#     """
#     Find positions of keyword phrases in OCR data with fuzzy matching.
#     """
#     matched_bboxes = []
#     idx = 0

#     while idx < len(all_words):
#         word_data = all_words[idx]
#         word_text = word_data.get("word", "").strip()

#         if not word_text:
#             idx += 1
#             continue

#         for keyword in keywords:
#             keyword_parts = keyword.split()
#             temp_match = []
#             temp_bboxes = []
#             match_idx = idx

#             for part in keyword_parts:
#                 if match_idx < len(all_words):
#                     candidate_word = all_words[match_idx].get("word", "").strip()
#                     similarity = fuzz.ratio(part.lower(), candidate_word.lower())

#                     if similarity >= 70:
#                         temp_match.append(part)
#                         temp_bboxes.append(all_words[match_idx].get("bbox", {}))
#                         match_idx += 1
#                     elif len(candidate_word) > len(part) and part in candidate_word:
#                         # Handle combined words
#                         similarity = fuzz.ratio(part.lower(), candidate_word[:len(part)].lower())
#                         if similarity >= 70:
#                             temp_match.append(part)
#                             temp_bboxes.append(all_words[match_idx].get("bbox", {}))
#                             all_words[match_idx]["word"] = candidate_word[len(part):]
#                             break
#                         else:
#                             temp_match = []
#                             temp_bboxes = []
#                             break

#                 else:
#                     temp_match = []
#                     temp_bboxes = []
#                     break

#             if temp_match == keyword_parts:
#                 matched_bboxes.extend(temp_bboxes)
#                 idx = match_idx - 1
#                 break

#         idx += 1

#     return matched_bboxes

# def Search(assistant_output, json_database_path):
#     assistant_data = preprocess_json(assistant_output)
#     assistant_data = fill_defaults(assistant_data)

#     description = assistant_data["Dialogue"]
#     highlighted = assistant_data["highlighted"]
#     emotion = assistant_data["ConversationStyle"]

#     output = [description]  # result[0]
#     titles, keywords, captions = [], [], []

#     try:
#         with open(json_database_path, 'r', encoding='utf-8') as f:
#             database = json.load(f)
#     except (FileNotFoundError, json.JSONDecodeError):
#         print(f"Error: Could not load database from {json_database_path}.")
#         return []

#     for item in highlighted:
#         group_id = str(item.get("id", ""))
#         highlight_type = item.get("type", "")
#         keywords_list = item.get("keywords", [])

#         group_data = next((data for data in database if str(data.get("group_id", "")) == group_id), None)
#         if not group_data:
#             print(f"Group ID {group_id} not found.")
#             continue

#         if highlight_type in ["小主题", "海报标题"]:
#             titles.append(group_data.get("bbox", {}))

#         elif highlight_type == "文本内容":
#             all_words = group_data.get("words", [])
#             matched_bboxes = find_keyword_positions(keywords_list, all_words)
#             keywords.append(matched_bboxes)

#         elif highlight_type == "图片描述":
#             captions.append(group_data.get("bbox", {}))

#     output.append(titles)
#     output.append(keywords)
#     output.append(captions)
#     output.append(emotion)
#     return output

import json
from fuzzywuzzy import fuzz

def preprocess_json(json_string):
    """
    Preprocess the JSON string to fix common format issues.
    """
    if json_string.startswith("```json"):
        json_string = json_string[7:].strip()
    if json_string.endswith("```"):
        json_string = json_string[:-3].strip()

    try:
        return json.loads(json_string)
    except json.JSONDecodeError:
        # Attempt to fix unquoted keys and values
        json_string = re.sub(r'(?<!")\b\w+\b(?=\s*:)','"\\g<0>"', json_string)
        json_string = re.sub(r':\s*(\b\w+\b)', r': "\\g<1>"', json_string)
        try:
            return json.loads(json_string)
        except json.JSONDecodeError:
            return {"highlighted": [], "ConversationStyle": "", "Dialogue": ""}

def fill_defaults(assistant_data):
    """
    Fill in default values for missing fields in the assistant data.
    """
    if not assistant_data.get("highlighted"):
        assistant_data["highlighted"] = []
    if not assistant_data.get("ConversationStyle"):
        assistant_data["ConversationStyle"] = "Unknown"
    if not assistant_data.get("Dialogue"):
        assistant_data["Dialogue"] = "Please clarify your question."
    return assistant_data

def find_keyword_positions(keywords, all_words):
    """
    Find positions of keyword phrases in OCR data with fuzzy matching.
    """
    matched_bboxes = []
    idx = 0

    while idx < len(all_words):
        word_data = all_words[idx]
        word_text = word_data.get("word", "").strip()

        if not word_text:
            idx += 1
            continue

        for keyword in keywords:
            keyword_parts = keyword.split()
            temp_match = []
            temp_bboxes = []
            match_idx = idx

            for part in keyword_parts:
                while match_idx < len(all_words):
                    candidate_word = all_words[match_idx].get("word", "").strip()
                    similarity = fuzz.ratio(part.lower(), candidate_word.lower())

                    if similarity >= 70:
                        temp_match.append(part)
                        temp_bboxes.append(all_words[match_idx].get("bbox", {}))
                        match_idx += 1
                        break
                    elif len(candidate_word) > len(part) and part in candidate_word:
                        # Handle combined words
                        similarity = fuzz.ratio(part.lower(), candidate_word[:len(part)].lower())
                        if similarity >= 70:
                            temp_match.append(part)
                            temp_bboxes.append(all_words[match_idx].get("bbox", {}))
                            all_words[match_idx]["word"] = candidate_word[len(part):]
                            break
                    else:
                        match_idx += 1
                else:
                    temp_match = []
                    temp_bboxes = []
                    break

            if temp_match == keyword_parts:
                matched_bboxes.extend(temp_bboxes)
                idx = match_idx - 1
                break

        idx += 1

    return matched_bboxes

def Search(assistant_output, json_database_path):
    assistant_data = preprocess_json(assistant_output)
    assistant_data = fill_defaults(assistant_data)

    description = assistant_data["Dialogue"]
    highlighted = assistant_data["highlighted"]
    emotion = assistant_data["ConversationStyle"]

    output = [description]  # result[0]
    titles, keywords, captions = [], [], []

    try:
        with open(json_database_path, 'r', encoding='utf-8') as f:
            database = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        print(f"Error: Could not load database from {json_database_path}.")
        return []

    for item in highlighted:
        group_id = str(item.get("id", ""))
        highlight_type = item.get("type", "")
        keywords_list = item.get("keywords", [])

        group_data = next((data for data in database if str(data.get("group_id", "")) == group_id), None)
        if not group_data:
            print(f"Group ID {group_id} not found.")
            continue

        if highlight_type in ["小主题", "海报标题"]:
            titles.append(group_data.get("bbox", {}))

        elif highlight_type == "文本内容":
            all_words = []
            for line in group_data.get("lines", []):
                all_words.extend(line.get("words", []))

            matched_bboxes = find_keyword_positions(keywords_list, all_words)
            keywords.append(matched_bboxes)

        elif highlight_type == "图片描述":
            captions.append(group_data.get("bbox", {}))

    output.append(titles)
    output.append(keywords)
    output.append(captions)
    output.append(emotion)
    return output

# assistantOutput = """
# {
#   "highlighted": [
#     {
#       "id": 6,
#       "text": "The Social Function of Design",
#       "type": "小主题"
#     },
#     {
#       "id": 8,
#       "text": "The social mission of design gained attention in the mid-1970s, prioritizing functionality and safety. Victor Papanek's Design for the Real World exemplified this, advocating for product designs that foster human interaction and address real-world needs, thus merging innovation with social responsibility to establish new design standards.",
#       "type": "文本内容",
#       "keywords": ["social mission", "functionality", "safety", "human interaction", "real-world needs"]
#     }
#   ],
#   "ConversationStyle": "01",
#   "Dialogue": "In the mid-1970s, design started to focus more on social functions, ensuring products were functional and safe. Victor Papanek's work 'Design for the Real World' highlighted how design could enhance human interaction and meet real-world needs. It's fascinating how design can blend innovation with social responsibility. Would you like to delve deeper into any specific designer's work or explore other aspects of design history presented here?"
# }
# """

# output = Search(assistantOutput, 'eval1_grouped.json')
# print(output)