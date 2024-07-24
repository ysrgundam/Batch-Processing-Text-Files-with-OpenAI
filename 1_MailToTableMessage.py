import os
import yaml
from openai import OpenAI
import httpx
import sys

TIMEOUT = 300  # 5分钟

# 读取配置文件
with open('config.yaml', 'r', encoding='utf-8') as file:
    config = yaml.safe_load(file)

# 从配置文件中读取API关键字和其他配置信息
api_key = config['openai']['api_key']
base_url = config['openai']['base_url']
model = config['openai']['model']
input_folder_path = config['input_folder']['path']
output_folder_path = config['output_messagefolder']['path']
prompt_text = config['prompt']['text']
max_tokens = config['max_tokens']

# 初始化OpenAI客户端
client = OpenAI(
    api_key=api_key, 
    base_url=base_url,
    http_client=httpx.Client(timeout=TIMEOUT)  # 设置HTTP客户端超时时间
)

# 处理流式响应的函数，将流式数据处理并拼接成完整响应
def process_stream(stream):
    full_response = ""
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:  # 检查chunk内容是否为空
            content = chunk.choices[0].delta.content
            print(content, end='', flush=True)  # 实时打印输出
            full_response += content  # 拼接内容到完整响应
    print()  # 换行
    return full_response

# 处理文件
for file_name in os.listdir(input_folder_path):  # 遍历输入文件夹中的所有文件
    if file_name.endswith('.html'):  # 只处理HTML文件
        file_path = os.path.join(input_folder_path, file_name)
        
        print(f"\nProcessing file: {file_name}")  # 打印当前处理的文件名
        
        with open(file_path, 'r', encoding='utf-8') as file:
            email_content = file.read()  # 读取文件内容
        
        # 构建prompt文本
        prompt = prompt_text.format(email_content=email_content)

        full_response = ""

        while True:
            # 使用流式API请求OpenAI生成内容
            stream = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens,
                stream=True  # 启用流式输出
            )

            # 处理流式响应并拼接成完整响应
            chunk_response = process_stream(stream)
            full_response += chunk_response

            if len(chunk_response.split()) < max_tokens:  # 判断是否达到最大token数
                break
            prompt = "続く：" + chunk_response.split()[-20:]  # 更新prompt，附加上一次响应的结尾

        # 保存生成的内容到输出文件夹中
        output_file_name = f"{os.path.splitext(file_name)[0]}.txt"
        output_file_path = os.path.join(output_folder_path, output_file_name)

        os.makedirs(output_folder_path, exist_ok=True)  # 确保输出文件夹存在

        with open(output_file_path, 'w', encoding='utf-8') as file:
            file.write(full_response)  # 写入完整响应

        print(f"\nOutput saved to {output_file_name}")  # 打印输出文件名

print("\nAll files processed.")  # 提示所有文件处理完毕