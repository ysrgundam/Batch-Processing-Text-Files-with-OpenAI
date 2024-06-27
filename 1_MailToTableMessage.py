import os
import yaml
from openai import OpenAI

def get_full_response(prompt):
    full_response = ""
    current_prompt = prompt
    while True:
        response = call_llm_api(current_prompt)
        full_response += response
        if len(response.split()) < 1000:  # 假设1000是max_tokens的设置
            break
        current_prompt = "继续：" + response.split()[-20:]  # 用最后的20个词作为新的提示
    return full_response

# 读取配置文件
with open('config.yaml', 'r', encoding='utf-8') as file:
    config = yaml.safe_load(file)

# 从配置文件获取参数
api_key = config['openai']['api_key']
base_url = config['openai']['base_url']
model = config['openai']['model']
input_folder_path = config['input_folder']['path']
output_folder_path = config['output_messagefolder']['path']
prompt_text = config['prompt']['text']
max_tokens = config['max_tokens']

# 初始化OpenAI客户端
client = OpenAI(api_key=api_key, base_url=base_url)

# 遍历输入文件夹中的所有.txt文件
for file_name in os.listdir(input_folder_path):
    if file_name.endswith('.html'):
        file_path = os.path.join(input_folder_path, file_name)
        
        # 读取文件内容
        with open(file_path, 'r', encoding='utf-8') as file:
            email_content = file.read()
        
        # 构建完整的prompt
        prompt = prompt_text.format(email_content=email_content)

        full_response = ""

        while True:
            # 创建聊天完成请求，加入max_tokens参数
            completion = client.chat.completions.create(
                model=model,  # 使用配置文件中的模型
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens  # 设置输出的最大token数
            )

            # 获取模型的输出并存储到变量
            model_output = completion.choices[0].message.content
            
            # 现在 model_output 变量包含了模型的输出
            print(model_output)

            full_response += model_output
            if len(model_output.split()) < max_tokens:
                break
            current_prompt = "続く：" + model_output.split()[-20:]  # 用最后的20个词作为新的提示

        # 为每个处理的文件生成一个唯一的输出文件名
        output_file_name = f"{os.path.splitext(file_name)[0]}.txt"
        output_file_path = os.path.join(output_folder_path, output_file_name)

        # 创建输出文件夹（如果不存在）
        os.makedirs(output_folder_path, exist_ok=True)

        # 打开一个文件进行写入
        with open(output_file_path, 'w', encoding='utf-8') as file:
            file.write(full_response)

        # 打印一条信息确认文件已被保存
        print(f"Output saved to {output_file_name}")