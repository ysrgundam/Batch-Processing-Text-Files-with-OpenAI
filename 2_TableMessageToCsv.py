import os
import yaml
import pandas as pd
from io import StringIO
import re
import csv
import codecs

# 读取配置文件
with open('config.yaml', 'r', encoding='utf-8') as file:
    config = yaml.safe_load(file)

# 从配置文件获取参数
input_folder_path = config['output_messagefolder']['path']
output_folder_path = config['output_csvfolder']['path']

# 遍历输入文件夹中的所有.txt文件
for file_name in os.listdir(input_folder_path):
    if file_name.endswith('.txt'):
        file_path = os.path.join(input_folder_path, file_name)
        
        # 读取文件内容
        with open(file_path, 'r', encoding='utf-8') as file:
            email_content = file.read()

        # 设置显示的最大列数
        pd.set_option('display.max_columns', None)

        # 设置显示的最大行数
        pd.set_option('display.max_rows', None)

        # 设置列宽，使得DataFrame中的数据不会被过早截断
        pd.set_option('display.max_colwidth', None)

        # 使用正则表达式找出表格部分
        pattern = r"紹介日\|提供元案件番号\|.*?(?=\n\n|$)"  # 假设表格每行以日期开头，后面不是数字的行标志表格结束
        table_content = '\n'.join(re.findall(pattern, email_content, re.DOTALL))

        # 预处理数据以处理连续的列分隔符
        table_content = re.sub(r'\|\|', '|empty|', table_content)

        # 将预处理后的表格字符串转换为DataFrame
        data_io = StringIO(table_content)
        try:
            df = pd.read_csv(data_io, sep='|')
        except pd.errors.ParserError as e:
            print(f"ParserError: {str(e)}")
            print("Data preprocessing failed to handle inconsistent separators.")

        print(df)

        # 创建输出文件夹（如果不存在）
        os.makedirs(output_folder_path, exist_ok=True)

        # 生成CSV文件的路径
        csv_file_name = f"extracted_data_utf-8_{os.path.splitext(file_name)[0]}.csv"
        csv_file_path = os.path.join(output_folder_path, csv_file_name)

        # 将DataFrame保存为CSV文件 (UTF-8 编码)
        df.to_csv(csv_file_path, index=False, encoding='utf-8')

        # 生成Shift_JIS编码的CSV文件的路径
        output_file_name = f"extracted_data_shiftjis_{os.path.splitext(file_name)[0]}.csv"
        output_file_path = os.path.join(output_folder_path, output_file_name)

        # 打开输入文件 (UTF-8 编码)
        with codecs.open(csv_file_path, 'r', 'utf-8') as file:
            reader = csv.reader(file)
            rows = list(reader)

        # 打开输出文件 (Shift_JIS 编码)
        with codecs.open(output_file_path, 'w', 'shift_jis') as file:
            writer = csv.writer(file)
            
            # 逐行写入转换后的数据
            for row in rows:
                encoded_row = [cell.encode('shift_jis', 'ignore').decode('shift_jis') for cell in row]
                writer.writerow(encoded_row)

        print(f"转换完成. 输出文件: {output_file_name}")