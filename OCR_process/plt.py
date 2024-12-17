import json
from PIL import Image, ImageDraw, ImageFont

# 加载 JSON 数据
with open("json_results/grouped_results.json", "r", encoding="utf-8") as f:
    grouped_data = json.load(f)

# 图像尺寸设定（白色背景）
image_width = 7000  # 根据海报文本范围设定
image_height = 5000
background_color = (255, 255, 255)  # 白色背景
font_color = (0, 0, 0)  # 黑色字体
bbox_color = (255, 0, 0)  # 红色边框

# 创建一个白色背景的图像
image = Image.new("RGB", (image_width, image_height), background_color)
draw = ImageDraw.Draw(image)

# 加载字体（系统字体路径，可根据实际环境调整）
try:
    font = ImageFont.truetype("PingFangSC-Regular.otf", 20)
except:
    print('未能成功加载字体，使用默认字体')
    font = ImageFont.load_default()  # 如果加载失败，使用默认字体

# 绘制边界框和文字
for item in grouped_data:
    text = item["text"]
    bbox = item["bbox"]  # 4个点的坐标：[[x_min, y_min], [x_max, y_min], [x_max, y_max], [x_min, y_max]]

    # 提取坐标
    x_min, y_min = bbox[0]
    x_max, y_max = bbox[2]

    # 画出边界框
    draw.rectangle([x_min, y_min, x_max, y_max], outline=bbox_color, width=2)

    # 在边界框的上方写入文字
    text_position = (x_min, y_min - 25)  # 防止文字覆盖边框
    draw.text(text_position, text, fill=font_color, font=font)

# 保存结果图像
output_path = "visualized_ocr_results.png"
image.save(output_path)
print(f"可视化结果已保存到 {output_path}")

# 可选：直接显示图像（需要环境支持 GUI）
image.show()