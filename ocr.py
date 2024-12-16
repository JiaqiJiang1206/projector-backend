from PIL import Image
import cv2
import easyocr
import json
import numpy as np

# 定义OCR处理函数
def preprocess_image(image_path):
    """
    图像预处理：灰度化和二值化
    """
    image = cv2.imread(image_path)  # 读取图像
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # 灰度化
    _, binary = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY)  # 二值化
    processed_image_path = "processed_image.jpg"
    cv2.imwrite(processed_image_path, binary)  # 保存预处理图像
    return processed_image_path

def perform_ocr(image_path, languages=['ch_sim', 'en']):
    """
    OCR文字识别并返回结果
    """
    reader = easyocr.Reader(languages)  # 初始化EasyOCR
    results = reader.readtext(image_path, detail=1)  # 识别文字
    structured_results = []  # 用于存储结构化结果
    
    for (bbox, text, prob) in results:
        # 将OCR结果结构化
        structured_results.append({
            "text": text,
            "bbox": [list(map(int, point)) for point in bbox],  # 转换为标准Python int
            "confidence": float(prob)  # 转换为Python float
        })
    return structured_results

def save_results_to_json(results, output_path="ocr_results.json"):
    """
    保存OCR结果为JSON文件，确保兼容JSON序列化
    """
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=4)

def main(image_path):
    """
    主流程函数：预处理图像，执行OCR，保存结果
    """
    print("开始图像预处理...")
    processed_image_path = preprocess_image(image_path)
    
    print("执行OCR识别...")
    results = perform_ocr(processed_image_path)
    
    print("识别结果:")
    for result in results:
        print(f"Text: {result['text']}, BBox: {result['bbox']}, Confidence: {result['confidence']}")
    
    print("保存结果为JSON文件...")
    save_results_to_json(results)
    print("处理完成，结果保存在 ocr_results.json 文件中！")

# 调用主流程
if __name__ == "__main__":
    image_path = "img/poster.png"  # 替换为你的图像路径
    main(image_path)
