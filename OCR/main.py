from block_to_line import block_to_line
from line_to_group import line_to_group
from draw_group import draw_group

def main():
  poster = "modern"

  ocr_results = f"json_results/{poster}_ocr_results.json"
  line_results = f"json_results/{poster}_line_results.json"
  group_results = f"json_results/{poster}_group_results.json"

  source_img = f"img/poster_{poster}.jpg"
  output_img = f"{poster}_final_result.jpg"
  # 1. 将文本块合并为文本行
  block_to_line(ocr_results, line_results, eps_y=10, eps_x=10)
  
  # 2. 将文本行合并为文本组
  line_to_group(line_results, group_results, eps=250)
  
  # 3. 可视化结果
  draw_group(group_results, output_img, source_img)
    
if __name__ == "__main__":
  main()