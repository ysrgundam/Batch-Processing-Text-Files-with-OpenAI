import pandas as pd
from io import StringIO
import re

# 读取本地文件
file_path = 'D:\\00_WIP\\07_AI_PowerAutomate\\Code\\MessageFile.txt'
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

# 将提取的表格字符串转换为DataFrame
data_io = StringIO(table_content)
df = pd.read_csv(data_io, sep='|')

print(df)

# 如果需要，可以将DataFrame保存为CSV文件
df.to_csv('extracted_data_utf8.csv', index=False, encoding='utf-8')

import csv
import codecs

# 输入文件名和输出文件名
input_file = 'extracted_data_utf8.csv'
output_file = 'extracted_data_shiftjis.csv'

# 打开输入文件 (UTF-8 编码)
with codecs.open(input_file, 'r', 'utf-8') as file:
    reader = csv.reader(file)
    rows = list(reader)

# 打开输出文件 (Shift_JIS 编码)
with codecs.open(output_file, 'w', 'shift_jis') as file:
    writer = csv.writer(file)
    
    # 逐行写入转换后的数据
    for row in rows:
        encoded_row = [cell.encode('shift_jis', 'ignore').decode('shift_jis') for cell in row]
        writer.writerow(encoded_row)

print(f"转换完成. 输出文件: {output_file}")