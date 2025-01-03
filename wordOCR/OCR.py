import onnxruntime as ort
ort.set_default_logger_severity(3)  # ERROR level 忽略 warning
from config import *
from crnn import CRNNHandle
# from angnet import AngleNetHandle
from utils import draw_bbox, crop_rect, sorted_boxes, get_rotate_crop_image
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import cv2
import copy
from dbnet.dbnet_infer import DBNET
import time
import traceback
import random
import os
import json
from line_to_group import line_to_group
import draw_group


class OcrHandle(object):
    def __init__(self):
        self.text_handle = DBNET(model_path)
        self.crnn_handle = CRNNHandle(crnn_model_path)
        # if angle_detect:
        #     self.angle_handle = AngleNetHandle(angle_net_path)

    def crnnRecWithBox(self, im, boxes_list, score_list):
        results = []
        boxes_list = sorted_boxes(np.array(boxes_list))
        for index, (box, score) in enumerate(zip(boxes_list, score_list)):
            tmp_box = copy.deepcopy(box)
            partImg_array = get_rotate_crop_image(im, tmp_box.astype(np.float32))
            partImg = Image.fromarray(partImg_array).convert("RGB")
            try:
                result = self.crnn_handle.predict_rbg(partImg, copy.deepcopy(box))  # 识别文本
            except Exception as e:
                print(f"警告: CRNN识别失败: {e}")
                result = ""
            bbox_list = tmp_box.tolist()
            results.append({'bbox': bbox_list, 'text': result, 'score': score})
        return results

    def text_predict(self, img, short_size):
        boxes_list, score_list = self.text_handle.process(np.asarray(img).astype(np.uint8), short_size=short_size)
        result = self.crnnRecWithBox(np.array(img), boxes_list, score_list)
        return result


def flatten(lst):
    """递归地将嵌套列表平铺为一维列表"""
    if isinstance(lst, list):
        return [a for i in lst for a in flatten(i)]
    else:
        return [lst]


def get_bbox_from_rect(rect):
    """
    根据rect的不同格式，返回标准的四个点坐标列表。
    支持的格式：
    1. [x_min, y_min, x_max, y_max]
    2. [[x_min, y_min], [x_max, y_max]]
    3. [x1, y1, x2, y2, x3, y3, x4, y4]
    4. [[x1, y1], [x2, y2], [x3, y3], [x4, y4]]
    """
    flat_rect = flatten(rect)

    if len(flat_rect) == 4 and all(isinstance(x, (int, float)) for x in flat_rect):
        # 格式1: [x_min, y_min, x_max, y_max]
        x_min, y_min, x_max, y_max = flat_rect
        return [
            [float(x_min), float(y_min)],
            [float(x_max), float(y_min)],
            [float(x_max), float(y_max)],
            [float(x_min), float(y_max)]
        ]
    elif len(flat_rect) == 8 and all(isinstance(x, (int, float)) for x in flat_rect):
        # 格式3: [x1, y1, x2, y2, x3, y3, x4, y4]
        x1, y1, x2, y2, x3, y3, x4, y4 = flat_rect
        return [
            [float(x1), float(y1)],
            [float(x2), float(y2)],
            [float(x3), float(y3)],
            [float(x4), float(y4)]
        ]
    else:
        print(f"警告: 无法解析的bbox格式: {rect}")
        return None


def get_color():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))


def convert_to_serializable(obj):
    """递归地将所有 numpy.ndarray 转换为列表"""
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, dict):
        return {k: convert_to_serializable(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_to_serializable(item) for item in obj]
    else:
        return obj


def get_char(image_path, output_path):
    # 硬编码参数
    # IMAGE_PATHS = ['images/0.png']  # 可以添加更多图像路径，例如 ['images/0.png', 'images/1.png']
    RECOGNITION_LEVEL = 'char'      # 选择 'char'、'word' 或 'line'
    # OUTPUT_JSON_PATH = 'output/bboxes2.json'

    # 创建输出目录
    os.makedirs('output', exist_ok=True)
    ocrhandle = OcrHandle()
    all_image_bboxes = {}

    for pic_idx, path in enumerate(image_path):
        short_size = 960
        try:
            img = Image.open(path).convert('RGB')
        except Exception as e:
            print(f"错误: 无法打开图像 {path}: {e}")
            continue

        print(f"Processing image: {path}, size: {np.array(img).shape}")
        res = ocrhandle.text_predict(img, short_size)

        img_detected = img.copy()
        img_draw = ImageDraw.Draw(img_detected)
        colors = ['red', 'green', 'blue', "purple"]

        all_bboxes = []

        for i, r in enumerate(res):
            rect, txt, confidence = r['bbox'], r['text'], r['score']
            print(f"rect: {rect}")  # 调试输出

            bbox = get_bbox_from_rect(rect)
            if bbox is None:
                continue

            # 计算字体大小
            if len(bbox) == 4:
                x_min, y_min = bbox[0]
                x_max, y_max = bbox[2]
                width = x_max - x_min
                height = y_max - y_min
                size = max(min(width, height) // 2, 15)
            else:
                print(f"警告: bbox点数不正确: {bbox}")
                size = 15

            try:
                myfont = ImageFont.truetype("仿宋_GB2312.ttf", size=size)
            except IOError:
                myfont = ImageFont.load_default()
                print("警告: 字体文件 '仿宋_GB2312.ttf' 未找到，使用默认字体。")

            fillcolor = get_color()

            # 将bbox和text保存到all_bboxes
            all_bboxes.append({'bbox': bbox, 'text': txt})

            if RECOGNITION_LEVEL == 'line':
                line_text = txt.get('line_pred', '')
                img_draw.text((x_min, y_min - size), str(line_text), font=myfont, fill=fillcolor)
                # 绘制矩形框
                img_draw.line([
                    (x_min, y_min),
                    (x_max, y_min),
                    (x_max, y_max),
                    (x_min, y_max),
                    (x_min, y_min)
                ], fill=fillcolor, width=2)

            elif RECOGNITION_LEVEL == 'char':
                for j, char_item in enumerate(txt.get('char_list', [])):
                    char = char_item.get('char', '')
                    line = char_item.get('line', ((0, 0), (0, 0)))
                    if len(line) == 2 and all(len(point) == 2 for point in line):
                        cx1, cy1 = line[0]
                        cx2, cy2 = line[1]
                        img_draw.text((cx1, cy1 - size), str(char), font=myfont, fill=fillcolor)
                    else:
                        print(f"警告: 无法解析字符的line坐标: {line}")

                    char_bbox = char_item.get('bbox', [])
                    char_bbox_formatted = get_bbox_from_rect(char_bbox)
                    if char_bbox_formatted:
                        # 绘制椭圆
                        if len(char_bbox_formatted) == 4:
                            x1_c, y1_c = char_bbox_formatted[0]
                            x3_c, y3_c = char_bbox_formatted[2]
                            img_draw.ellipse([(x1_c, y1_c), (x3_c, y3_c)], outline=get_color())
                        else:
                            print(f"警告: 字符bbox_formatted 点数不正确: {char_bbox_formatted}")

            elif RECOGNITION_LEVEL == 'word':
                word_text = txt.get('words', [])
                for j, word in enumerate(word_text):
                    word_bbox = word.get('bbox', [])
                    word_value = word.get('value', '')
                    word_bbox_formatted = get_bbox_from_rect(word_bbox)
                    if word_bbox_formatted:
                        all_bboxes.append({'bbox': word_bbox_formatted, 'text': word_value})
                        color = get_color()
                        # 绘制椭圆
                        if len(word_bbox_formatted) == 4:
                            wx1, wy1 = word_bbox_formatted[0]
                            wx3, wy3 = word_bbox_formatted[2]
                            img_draw.ellipse([(wx1, wy1), (wx3, wy3)], outline=color)
                            img_draw.text((wx1, wy1 - size), str(word_value), font=myfont, fill=color)
                        else:
                            print(f"警告: word_bbox_formatted 点数不正确: {word_bbox_formatted}")

        # 存储当前图片的所有bbox和对应的文本
        all_image_bboxes[path] = all_bboxes

        # 打印所有bbox和对应的文本
        print(f"位置和对应的文本: {all_bboxes}")

        img_detected = img_detected.convert('RGB')
        output_image_path = f'output/{pic_idx:02}.jpg'
        try:
            img_detected.save(output_image_path, format='JPEG')
            print(f"已保存处理后的图像到 {output_image_path}")
        except Exception as e:
            print(f"错误: 无法保存图像 {output_image_path}: {e}")

    # 将所有数据转换为可序列化的类型
    serializable_bboxes = convert_to_serializable(all_image_bboxes)

    # 保存所有图片的bbox和对应的文本到JSON文件
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(serializable_bboxes, f, ensure_ascii=False, indent=4)
        print(f"所有bbox和对应的文本已保存到 {output_path}")
    except Exception as e:
        print(f"错误: 无法保存JSON文件 {output_path}: {e}")


def modify_json(input_file, output_file):
    # 读取原始JSON文件
    with open(input_file, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # 获取 list
    image_data_list = data.get("images/eval1.png", [])

    # 建立新的数据结构数组
    new_data_list = []
    for item in image_data_list:
        modified_item = {
            "line_pred": item["text"]["line_pred"],
            "bbox": item["bbox"],
            "words": item["text"]["words"]
        }
        new_data_list.append(modified_item)

    # 将修改后的数据数组写到新的JSON文件
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(new_data_list, file, indent=4, ensure_ascii=False)

def construct_only_group(input_file, output_file):
    # 读取原始JSON文件
    with open(input_file, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # 建立新的数据结构数组
    new_data_list = []
    for item in data:
        new_item = {
            "id": item["group_id"],
            "text": item["text"]
        }
        new_data_list.append(new_item)

    # 将修改后的数据数组写到新的JSON文件
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(new_data_list, file, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    input_img_path = "images/eval1.png"
    # 基于当前输入图片的文件名，生成输出 JSON 文件的文件名，并且表示出保存的是原始数据
    raw_output_json = f"output/{os.path.basename(input_img_path).split('.')[0]}_raw_char.json"
    get_char([input_img_path], raw_output_json)
    # 将原始 OCR 输出的 JSON 变为含有 line_pred 和 words 的 JSON 列表
    line_output_json = f"output/{os.path.basename(input_img_path).split('.')[0]}_line.json"
    modify_json(raw_output_json, line_output_json)
    # 将含有 line_pred 和 words 的 JSON 列表转换为分组的 JSON 文件
    grouped_output_json = f"output/{os.path.basename(input_img_path).split('.')[0]}_grouped.json"
    line_to_group([line_output_json], grouped_output_json, 200)
    # 绘制分组的 JSON 文件
    output_img_path = f"output/{os.path.basename(input_img_path).split('.')[0]}_vis.jpg"
    draw_group.draw_group(grouped_output_json, output_img_path, input_img_path)
    # 将 group 中的 id 和 text 写到新的 JSON 文件中
    only_group_output_json = f"output/{os.path.basename(input_img_path).split('.')[0]}_only_group.json"
    construct_only_group(grouped_output_json, only_group_output_json)
    