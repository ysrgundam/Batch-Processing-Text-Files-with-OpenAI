import csv

# 指定测试用例文件的路径
file_path = "D:\\00_WIP\\07_AI_PowerAutomate\\Batch-Processing-Text-Files-with-OpenAI\\OutputMessage\\20240613104557_【RPA転送】【SAP】案件情報_20240426.pdf.txt"

with open(file_path, 'r', encoding='utf-8') as file:
    markdown_data = file.read().strip().split('\n')

# 将Markdown表格转换为CSV格式
def markdown_to_csv(markdown_data):
    csv_data = []
    for line in markdown_data:
        # 移除行首行尾的竖线，并根据竖线分割数据
        stripped_line = line.strip('|').strip()
        columns = [col.strip() for col in stripped_line.split('|')]
        csv_data.append(columns)
    
    # 移除表头下的分隔线
    csv_data.pop(1)

    # 写入CSV文件
    with open('output.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(csv_data)

# 调用函数
markdown_to_csv(markdown_data)
