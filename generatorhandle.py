import json

def GeneratorHandler(input_json):
    try:
        # 将 JSON 字符串解析为字典
        input_json = json.loads(input_json)
        
        # 提取 return1 和 return2
        return1 = {
            "keyinfo": input_json.get("keyinfo", []),
            "connections": input_json.get("connections", [])
        }
        return2 = input_json.get("message", "")
        
        return return1, return2
    except json.JSONDecodeError as e:
        # 如果解析失败，返回错误信息
        return None, f"Invalid JSON string: {str(e)}"

# # 示例输入
# json_string = '''
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
#   "message": "20世纪80年代为设计带来了大胆的变革，后现代主义以其玩味美学为主导，孟菲斯设计小组以鲜艳的色彩和几何图案掀起风潮。“创意废旧”运动则以粗犷、朋克风格挑战传统设计规则。同时，数字革命在苹果Macintosh的引领下，彻底改变了创作流程。这一时期，品牌逐渐成为文化符号，塑造身份与生活方式，体现了向以形象为核心的消费文化的转变。"
# }
# '''

# # 调用方法
# return1, return2 = GeneratorHandler(json_string)

# # 输出结果
# print("Return 1:", json.dumps(return1, ensure_ascii=False, indent=2))
# print("Return 2:", return2)