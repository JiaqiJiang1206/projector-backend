from config import systemPromptPickerAgent1, systemPromptPickerAgent2, systemPromptPickerAgent3
from chatbot import ChatBot
import json

def Search(assistant_output: str, json_database_path: str):
    # 将字符串解析为 JSON
    assistant_data = json.loads(assistant_output)
    description = assistant_data["Dialogue"]
    highlighted = assistant_data["highlighted"]
    emotion = assistant_data["Emotion"]  # 直接获取字符串格式的 Emotion
    output = [description]  # 初始化输出列表
    bbox_list = []  # 存储所有 bbox 数据

    # 加载数据库
    with open(json_database_path, 'r', encoding='utf-8') as f:
        database = json.load(f)

    # 遍历 highlighted 部分
    for item in highlighted:
        group_id = str(item["id"])  # 转为字符串以匹配 JSON 数据
        highlight_type = item["type"]
        keywords = item.get("keywords", [])

        # 查找 group_id 对应的数据
        group_data = next((data for data in database if str(data["group_id"]) == group_id), None)
        if not group_data:
            print(f"Group ID {group_id} not found.")
            continue

        if highlight_type != "文本内容":
            # 如果类型不是 "文本内容"，直接添加 bbox
            bbox_list.append(group_data["bbox"])
        else:
            # 如果是 "文本内容"，匹配关键词并处理跨行逻辑
            matched_bboxes = []
            all_words = []  # 用于存储所有行的 words 数据
            for line in group_data.get("lines", []):
                all_words.extend(line.get("words", []))  # 聚合所有行的 words

            # 遍历关键词
            for keyword in keywords:
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
                        temp_match.append(word_data["bbox"])
                        if len(temp_match) == keyword_length:  # 完成一个关键词匹配
                            keyword_bboxes.extend(temp_match)
                            temp_match = []  # 重置临时匹配
                    else:
                        temp_match = []  # 重置匹配状态

                    word_index += 1

                # 如果找到关键词的 bbox，添加到结果中
                if keyword_bboxes:
                    matched_bboxes.extend(keyword_bboxes)

            # 添加匹配到的 bbox 数据
            if matched_bboxes:
                bbox_list.extend(matched_bboxes)
            else:
                print(f"No matching keywords found for group_id={group_id}.")

    output.append(bbox_list)
    output.append(emotion)  # 直接添加字符串格式的 Emotion
    return output


# posterTalker = ChatBot(systemPrompt=systemPromptPickerAgent, model="qwen-turbo")  
# content = """
# 品牌崛起还有什么。
# 严格按照要求的json格式输出
# """
# posterTalker.add_user_message(content)
# assistantOutput = """
# {
#   "highlighted": [
#     {
#       "id": 6,
#       "text": "新浪潮平面设计",
#       "type": "小主题"
#     },
#     {
#       "id": 7,
#       "text": "新浪潮平面设计起源于反对瑞士现代主义的传统阴 格结构。设计师通过利用层次和丰富的图像参考来 打破常规，增加互动性及动态的视觉效果，这使得 新波设计更具活力和趣味性。这样一种设计风格被 广泛应用于广告、音乐海报和主流媒体中，增强了 观众的视觉参与感",
#       "type": "文本内容",
#       "keywords": ["瑞士现代主义", "层次", "图像参考", "打破常规", "互动性"]
#     },
#     {
#       "id": 8,
#       "text": "彼得.夏尔于1984年左右设计的秘泉桌体现了加州新 浪潮设计风格。",
#       "type": "图片描述"
#     }
#   ],
#   "Dialogue": "新浪潮平面设计真的很有趣！它打破了传统的设计规则，加入了更多互动性和动态元素，让设计更加生动有趣。你看彼得·夏尔设计的‘秘泉’桌，是不是充满了创意？你觉得这种设计风格在当今数字化时代会有什么新的发展呢？右边还有一些扩展内容，可以让你了解更多关于这个时期的创新设计。",
#   "Emotion": "00"
# }
# """
# # print(assistantOutput)


# output = Search(assistantOutput, '0_grouped.json')
# print(output)


