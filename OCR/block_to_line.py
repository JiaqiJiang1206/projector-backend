import json
import numpy as np
from sklearn.cluster import DBSCAN
import os

def block_to_line(input_path, output_path, eps_y=10, eps_x=10):
    """将 textblock 变为 lineblock

    Args:
        input_path (_type_): 原始 OCR 结果的 JSON 文件路径
        output_path (_type_): 处理后 lineblock 的 JSON 文件路径
        eps_y (int, optional): 按照 y 坐标进行分组时 y 方向的阈值. Defaults to 10.
        eps_x (int, optional): 能够分为一组的左右距离的阈值. Defaults to 10.
    """
    # 加载 OCR 结果
    with open(input_path, "r", encoding="utf-8") as f:
        ocr_data = json.load(f)

    # 提取文本块的坐标和文本内容
    text_blocks = []
    for item in ocr_data:
        bbox = item["bbox"]
        x_left = bbox[0][0]
        x_right = bbox[1][0]
        y_center = (bbox[0][1] + bbox[3][1]) / 2
        height = abs(bbox[3][1] - bbox[0][1])
        text_blocks.append({
            "text": item["text"],
            "x_left": x_left,
            "x_right": x_right,
            "y_center": y_center,
            "height": height,
            "bbox": bbox,
            "blockid": item["blockid"]  # 保存原始的 blockid
        })

    # 将文本块按 y 坐标进行初步分组
    y_coords = np.array([[block["y_center"]] for block in text_blocks])
    eps_y = 10 #np.mean([block["height"] for block in text_blocks]) * 1.5  # y 坐标阈值
    y_clustering = DBSCAN(eps=eps_y, min_samples=1).fit(y_coords)
    y_labels = y_clustering.labels_

    # 将文本块按行分组
    grouped_lines = {}
    for idx, label in enumerate(y_labels):
        if label not in grouped_lines:
            grouped_lines[label] = []
        grouped_lines[label].append(text_blocks[idx])

    # 在每行内按 x 坐标排序，并拼接文本
    processed_lines = []
    for line_idx, (label, line_blocks) in enumerate(grouped_lines.items()):
        # 给每个 line 添加 id
        line_id = f"line_{str(line_idx + 1).zfill(2)}"
        
        # 按 x 坐标排序
        line_blocks = sorted(line_blocks, key=lambda block: block["x_left"])
        
        # 水平拼接文本块
        merged_text = line_blocks[0]["text"]
        current_bbox = line_blocks[0]["bbox"]
        current_x_right = line_blocks[0]["x_right"]
        belong_to_block = line_blocks[0]["blockid"]  # 标记第一块文本所属的 block

        for i in range(1, len(line_blocks)):
            block = line_blocks[i]
            # 判断水平间隔是否小于阈值（如当前文本块宽度的 0.5 倍）
            if block["x_left"] - current_x_right < eps_x: #(block["x_right"] - block["x_left"]) * 0.5:
                # 拼接文本
                merged_text += " " + block["text"]
                # 更新 bbox 范围（左右扩展）
                current_bbox[1][0] = max(current_bbox[1][0], block["bbox"][1][0])  # 更新右侧坐标
                current_bbox[2][0] = max(current_bbox[2][0], block["bbox"][2][0])
                # 记录所属的 block（如果不一样就保持原有的）
                belong_to_block = block["blockid"]
            else:
                # 保存当前拼接结果
                processed_lines.append({
                    "lineid": line_id,
                    "text": merged_text,
                    "bbox": current_bbox,
                    "belongtoblock": belong_to_block  # 记录该行所属的 block
                })
                # 开始新的文本块
                merged_text = block["text"]
                current_bbox = block["bbox"]
                belong_to_block = block["blockid"]
            current_x_right = block["x_right"]
        
        # 保存最后的拼接结果
        processed_lines.append({
            "lineid": line_id,
            "text": merged_text,
            "bbox": current_bbox,
            "belongtoblock": belong_to_block  # 记录该行所属的 block
        })
        # 输出为新的 JSON 文件,确保目标文件夹存在
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(processed_lines, f, ensure_ascii=False, indent=4)


    print(f"预处理完成，结果已保存到 {output_path}")

#test
block_to_line("ocr_results_block.json", "json_results/ocr_results_with_line.json")
