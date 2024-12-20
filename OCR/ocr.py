from PIL import Image
import cv2
import easyocr
import json
import numpy as np

# 定义OCR处理函数
def preprocess_image(image_path):
    """
    图像预处理：灰度化、去噪（高斯模糊）、直方图均衡化和二值化
    """
    image = cv2.imread(image_path)  # 读取图像
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # 灰度化

    # 高斯模糊，减少噪声
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # 直方图均衡化，增加图像对比度
    equalized = cv2.equalizeHist(blurred)

    # 二值化
    _, binary = cv2.threshold(equalized, 128, 255, cv2.THRESH_BINARY)

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

def save_results_to_json(results, output_path):
    """
    保存OCR结果为JSON文件，确保兼容JSON序列化
    """
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=4)

def run_ocr(image_path, output_path_with_confidence, output_path_with_blockid):
    """
    主流程函数：预处理图像，执行OCR，保存结果
    """
    print("开始图像预处理...")
    processed_image_path = image_path
    
    print("执行OCR识别...")
    results = perform_ocr(processed_image_path)
    
    print("识别结果:")
    for result in results:
        print(f"Text: {result['text']}, BBox: {result['bbox']}, Confidence: {result['confidence']}")
    
    # 保存包含confidence的结果
    print(f"保存结果为JSON文件（含confidence）...")
    save_results_to_json(results, output_path_with_confidence)
    
    # 处理不含confidence的结果，并加上block标签
    results_without_confidence = []
    for idx, result in enumerate(results):
        result_without_confidence = {
            "text": result["text"],
            "bbox": result["bbox"],
            "blockid": f"block_{str(idx + 1).zfill(2)}"
        }
        results_without_confidence.append(result_without_confidence)

    # 保存不含confidence的结果
    print(f"保存结果为JSON文件（不含confidence）...")
    save_results_to_json(results_without_confidence, output_path_with_blockid)
    print(f"处理完成，结果分别保存在 {output_path_with_confidence} 和 {output_path_with_blockid} 文件中！")


if __name__ == "__main__":
    image_path = "img/poster_modern_cn.jpg"
    output_path1 = "ocr_results.json"
    output_path2 = "ocr_results_without_confidence.json"
    run_ocr(image_path, output_path1, output_path2)