import json
import numpy as np
from sklearn.cluster import DBSCAN
import os

def line_to_group(input_path, output_path, eps=250):
  """_summary_

  Args:
      input_path (string): lineblock 的 JSON 文件路径
      output_path (string): 处理后的 groupblock 的 JSON 文件路径
      eps (int, optional): DBSCAN 聚类算法的参数，控制聚合范围. Defaults to 250.

  """

  # 加载 OCR 结果
  with open(input_path, "r", encoding="utf-8") as f:
      ocr_data = json.load(f)

  # 提取文本行的左上角坐标和高度
  coordinates = []
  for item in ocr_data:
      bbox = item["bbox"]
    #   x_center = (bbox[0][0] + bbox[1][0]) / 2
    #   y_center = (bbox[0][1] + bbox[3][1]) / 2
      coordinates.append([bbox[0][0], bbox[0][1]])

  coordinates = np.array(coordinates)

  # 使用 DBSCAN 聚类算法对文本块进行分组
  clustering = DBSCAN(eps, min_samples=1).fit(coordinates)  # eps 控制聚合范围
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
  for idx, texts in enumerate(grouped_texts.values(),start=1):
      texts = sorted(texts, key=lambda x: x["bbox"][0][1])  # 按 y 坐标排序
      merged_text = " ".join([t["text"] for t in texts])
      merged_bbox = merge_bboxes([t["bbox"] for t in texts])
      grouped_sentences.append({
          "id":idx,
          "text": merged_text,
          "bbox": merged_bbox
      })

  # 确保目标文件夹存在
  os.makedirs(os.path.dirname(output_path), exist_ok=True)
  with open(output_path, "w", encoding="utf-8") as f:
      json.dump(grouped_sentences, f, ensure_ascii=False, indent=4)

  print(f"处理完成，结果已保存到 {output_path}")