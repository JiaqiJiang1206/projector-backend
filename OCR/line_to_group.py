import json
import numpy as np
from sklearn.cluster import DBSCAN
import os

# 加载 OCR 结果
with open("json_results/line_results_modern.json", "r", encoding="utf-8") as f:
    ocr_data = json.load(f)

# 提取文本块的中心坐标和高度
coordinates = []
for item in ocr_data:
    bbox = item["bbox"]
    x_center = (bbox[0][0] + bbox[1][0]) / 2
    y_center = (bbox[0][1] + bbox[3][1]) / 2
    coordinates.append([x_center, y_center])

coordinates = np.array(coordinates)

# 使用 DBSCAN 聚类算法对文本块进行分组
clustering = DBSCAN(eps=250, min_samples=1).fit(coordinates)  # eps 控制聚合范围
grouped_texts = {}

for idx, label in enumerate(clustering.labels_):
    if label not in grouped_texts:
        grouped_texts[label] = []
    grouped_texts[label].append({
        "text": ocr_data[idx]["text"],
        "bbox": ocr_data[idx]["bbox"]
    })

# 合并文本和 bbox
def merge_bboxes(bboxes):
    """
    合并多个 bbox，返回一个外包围合并后的 bbox。
    """
    x_min = min(bbox[0][0] for bbox in bboxes)
    y_min = min(bbox[0][1] for bbox in bboxes)
    x_max = max(bbox[1][0] for bbox in bboxes)
    y_max = max(bbox[3][1] for bbox in bboxes)
    return [[x_min, y_min], [x_max, y_min], [x_max, y_max], [x_min, y_max]]

# 处理每一组，拼接文本并合并 bbox
grouped_sentences = []
for texts in grouped_texts.values():
    texts = sorted(texts, key=lambda x: x["bbox"][0][1])  # 按 y 坐标排序
    merged_text = " ".join([t["text"] for t in texts])
    merged_bbox = merge_bboxes([t["bbox"] for t in texts])
    grouped_sentences.append({
        "text": merged_text,
        "bbox": merged_bbox
    })

# 保存结果为 JSON 文件
output_path = "json_results/grouped_results.json"
# 确保目标文件夹存在
os.makedirs(os.path.dirname(output_path), exist_ok=True)
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(grouped_sentences, f, ensure_ascii=False, indent=4)

print(f"处理完成，结果已保存到 {output_path}")