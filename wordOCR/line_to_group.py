import json
import numpy as np
from sklearn.cluster import DBSCAN
import os

def convert_to_builtin_types(obj):
  if isinstance(obj, dict):
    return {key: convert_to_builtin_types(value) for key, value in obj.items()}
  elif isinstance(obj, list):
    return [convert_to_builtin_types(element) for element in obj]
  elif isinstance(obj, np.integer):  # NumPy 的 int 类型
    return int(obj)
  elif isinstance(obj, np.floating):  # NumPy 的 float 类型
    return float(obj)
  else:
    return obj

def merge_bboxes(bboxes):
  # 合并多个bbox，返回外包围合并后的bbox
  x_min = int(min(bbox[0][0] for bbox in bboxes))
  y_min = int(min(bbox[0][1] for bbox in bboxes))
  x_max = int(max(bbox[2][0] for bbox in bboxes))
  y_max = int(max(bbox[2][1] for bbox in bboxes))
  return [[x_min, y_min], [x_max, y_max]]

def line_to_group(file_list, output_path, eps=250):
  grouped_results = []

  for input_path in file_list:
    # 加载OCR结果
    with open(input_path, "r", encoding="utf-8") as f:
      ocr_data = json.load(f)

    # 提取文本行的左上角坐标
    coordinates = []
    for item in ocr_data:
      bbox = item["bbox"]
      coordinates.append([int(bbox[0][0]), int(bbox[0][1])])

    coordinates = np.array(coordinates)

    # 使用DBSCAN聚类算法对文本块进行分组
    clustering = DBSCAN(eps, min_samples=1).fit(coordinates)
    grouped_texts = {}

    for idx, label in enumerate(clustering.labels_):
      if label not in grouped_texts:
        grouped_texts[label] = []

      grouped_texts[label].append(ocr_data[idx])

    # 处理每一组，拼接文本并合并bbox
    for group_id, texts in grouped_texts.items():
      merged_bbox = merge_bboxes([t["bbox"] for t in texts])
      merged_text = " ".join(t["line_pred"] for t in texts)
      lines = []
      words = []

      for text in texts:
        line_bbox = merge_bboxes([text["bbox"]])
        line_words = []
        for word in text["words"]:
          word_bbox = merge_bboxes([word["bbox"]])
          line_words.append({
            "word": word.get("value", ""),  # 使用 get 方法提供默认值
            "bbox": word_bbox
          })
        lines.append({
          "line_pred": text["line_pred"],
          "bbox": line_bbox,
          "words": line_words
        })
        words.extend(line_words)

      grouped_results.append({
        "group_id": group_id,
        "text": merged_text,
        "bbox": merged_bbox,
        "lines": lines,  # 包含每一行的详细信息
        "words": words   # 所有行的words合并在一起
      })

  grouped_results = convert_to_builtin_types(grouped_results)
  
  # 确保目标文件夹存在
  os.makedirs(os.path.dirname(output_path), exist_ok=True)
  with open(output_path, "w", encoding="utf-8") as f:
    json.dump(grouped_results, f, ensure_ascii=False, indent=4)

  print(f"处理完成，结果已保存到 {output_path}")

# 使用示例
# input_files = ["output/modified.json"]  # 替换为你的 JSON 文件路径列表
# output_file = "output/grouped_output.json"
# line_to_group(input_files, output_file)