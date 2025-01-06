from dotenv import load_dotenv
import os
import dashscope
from dashscope import Assistants

# 这个脚本是操作生成思维导图的assistant的脚本，只有在需要修改的时候才可以把修改assistant的代码取消注释然后运行。其他时候不用管。
# qwen的assistant和其他chatbot的创建逻辑不太一样。类似于openai的assistant，但没有现成的playground界面，所以只能在代码里修改prompt等参数。


load_dotenv()
os.environ['DASHSCOPE_API_KEY'] = 'sk-da762947f89040b0895a6099f807bf62'
dashscope.api_key = "sk-da762947f89040b0895a6099f807bf62"


# # # 这里查看assistant的参数信息
# 