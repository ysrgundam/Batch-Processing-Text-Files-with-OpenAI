import os
import yaml
from openai import OpenAI
import httpx
import sys

TIMEOUT = 300  # 5分钟

# 读取配置文件
with open('config.yaml', 'r', encoding='utf-8') as file:
    config = yaml.safe_load(file)

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
    http_client=httpx.Client(timeout=TIMEOUT)
)

def process_stream(stream):
    full_response = ""
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            content = chunk.choices[0].delta.content
            print(content, end='', flush=True)
            full_response += content
    print()  # 换行
    return full_response

# 处理文件
for file_name in os.listdir(input_folder_path):
    if file_name.endswith('.html'):
        file_path = os.path.join(input_folder_path, file_name)
        
        print(f"\nProcessing file: {file_name}")
        
        with open(file_path, 'r', encoding='utf-8') as file:
            email_content = file.read()
        
        prompt = prompt_text.format(email_content=email_content)

        full_response = ""

        while True:
            # 使用流式API
            stream = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens,
                stream=True  # 启用流式输出
            )

            chunk_response = process_stream(stream)
            full_response += chunk_response

            if len(chunk_response.split()) < max_tokens:
                break
            prompt = "続く：" + chunk_response.split()[-20:]

        # 保存输出
        output_file_name = f"{os.path.splitext(file_name)[0]}.txt"
        output_file_path = os.path.join(output_folder_path, output_file_name)

        os.makedirs(output_folder_path, exist_ok=True)

        with open(output_file_path, 'w', encoding='utf-8') as file:
            file.write(full_response)

        print(f"\nOutput saved to {output_file_name}")

print("\nAll files processed.")