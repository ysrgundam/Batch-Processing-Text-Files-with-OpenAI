import subprocess
import os
import yaml

# 定义一个函数，用于将数据导入到Kintone应用中
def import_data_to_kintone(domain, app_id, api_token, csv_file_path):
    """
    将CSV文件的数据导入到Kintone应用中。
    :param domain: Kintone的域名
    :param app_id: 应用ID
    :param api_token: API令牌
    :param csv_file_path: 要导入的CSV文件路径
    :return: 表示导入是否成功的布尔值
    """
    # 构建命令行参数列表
    cli_command = [
        "cli-kintone.exe",  # Kintone命令行工具
        "--import",  # 导入操作
        "-d", domain,  # 指定域名
        "-a", str(app_id),  # 指定应用ID
        "-t", api_token,  # 指定API令牌
        "-f", csv_file_path,  # 指定CSV文件路径
        "-e", "utf-8"  # 指定文件编码
    ]
    try:
        # 执行命令行工具，导入数据
        result = subprocess.run(cli_command, check=True, capture_output=True, text=True, encoding='utf-8')
        print("数据导入成功:")
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        # 如果导入过程中出现错误，打印错误信息
        print("数据导入失败:")
        print(e.output)
        return False

# 打开并读取config.yaml配置文件
with open('config.yaml', 'r', encoding='utf-8') as file:
    config = yaml.safe_load(file)

# 从配置文件中获取必要的参数
domain = config['kintone']['domain']  # Kintone域名
app_id = config['kintone']['app_id']  # 应用ID
api_token = config['kintone']['api_token']  # API令牌
output_folder_path = config['output_csvfolder']['path']  # CSV文件输出文件夹路径

# 在指定文件夹中查找所有以'_utf8.csv'结尾的UTF-8编码的CSV文件
csv_files = [f for f in os.listdir(output_folder_path) if f.endswith('_utf8.csv')]

successful_imports = 0  # 成功导入的文件计数
total_files = len(csv_files)  # 总文件数

if csv_files:
    for csv_file_name in csv_files:
        # 构建完整的CSV文件路径
        csv_file_path = os.path.join(output_folder_path, csv_file_name)
        print(f"正在处理文件: {csv_file_name}")
        print(repr(domain))
        print(repr(app_id))
        print(repr(api_token))
        print(repr(csv_file_path))
        # 调用函数导入数据，如果成功则增加计数
        if import_data_to_kintone(domain, app_id, api_token, csv_file_path):
            successful_imports += 1
else:
    print("未找到UTF-8编码的CSV文件。")

# 打印处理结果摘要
print(f"\n处理完成: 共{total_files}个文件中，{successful_imports}个文件成功上传。")