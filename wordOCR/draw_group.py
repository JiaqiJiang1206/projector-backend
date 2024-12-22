import json
from PIL import Image, ImageDraw, ImageFont

def draw_group(group_json_path, output_path, image_path):
    # 加载 JSON 数据
    with open(group_json_path, "r", encoding="utf-8") as f:
        grouped_data = json.load(f)
    
    # 加载图像并计算图像尺寸
    image = Image.open(image_path).convert("RGB")
    draw = ImageDraw.Draw(image)

    font_color = (0, 0, 0)  # 黑色字体
    bbox_color = (255, 0, 0)  # 红色边框

    # 加载字体（系统字体路径，可根据实际环境调整）
    try:
        font = ImageFont.truetype("仿宋_GB2312.ttf", 20)
    except:
        print('未能成功加载字体，使用默认字体')
        font = ImageFont.load_default()  # 如果加载失败，使用默认字体

    # 绘制边界框和文字
    for item in grouped_data:
        text = item["text"]
        bbox = item["bbox"]  # 左上角和右下角坐标：[[x_min, y_min], [x_max, y_max]]

        # 提取坐标
        x_min, y_min = bbox[0]
        x_max, y_max = bbox[1]

        # 画出边界框
        draw.rectangle([x_min, y_min, x_max, y_max], outline=bbox_color, width=2)

        # 在边界框的上方写入文字
        text_position = (x_min, y_min - 25)  # 防止文字覆盖边框
        draw.text(text_position, text, fill=font_color, font=font)

    # 保存结果图像
    image.save(output_path)
    print(f"可视化结果已保存到 {output_path}")

    # 可选：直接显示图像（需要环境支持 GUI）
    image.show()