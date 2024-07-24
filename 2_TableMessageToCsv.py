# 导入所需的模块
import os  # 用于操作文件系统
import shutil  # 用于高级文件操作，如复制文件
import yaml  # 用于读取YAML配置文件
import logging  # 用于日志记录
from datetime import datetime  # 用于获取当前时间

# 设置日志记录
def setup_logging(log_folder):
    # 创建日志文件夹（如果不存在）
    os.makedirs(log_folder, exist_ok=True)
    # 获取当前时间，并格式化为字符串
    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    # 创建日志文件路径
    log_file = os.path.join(log_folder, f"file_converter_{current_time}.log")
    
    # 配置日志记录
    logging.basicConfig(
        level=logging.DEBUG,  # 设置日志级别为DEBUG
        format='%(asctime)s - %(levelname)s - %(message)s',  # 设置日志格式
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),  # 将日志写入文件
            logging.StreamHandler()  # 将日志输出到控制台
        ]
    )
    
    # 记录日志文件的创建位置
    logging.info(f"Log file created at: {log_file}")

# 读取配置文件
def read_config(config_path='config.yaml'):
    try:
        # 打开并读取YAML配置文件
        with open(config_path, 'r', encoding='utf-8') as file:
            return yaml.safe_load(file)
    except Exception as e:
        # 如果读取过程中出现错误，记录错误信息
        logging.error(f"Error reading config file: {str(e)}")
        return None

# 复制并重命名文件
def copy_and_rename(src_path, dest_path):
    try:
        # 使用shutil.copy2复制文件，保留元数据
        shutil.copy2(src_path, dest_path)
        # 记录成功信息
        logging.info(f"File copied and renamed: {dest_path}")
    except Exception as e:
        # 如果复制过程中出现错误，记录错误信息
        logging.error(f"Error copying file {src_path}: {str(e)}")

# 将文件转换为Shift-JIS编码
def convert_to_shift_jis(src_path, dest_path):
    try:
        # 以UTF-8编码读取源文件
        with open(src_path, 'r', encoding='utf-8') as src_file:
            content = src_file.read()
        
        # 以Shift-JIS编码写入目标文件
        with open(dest_path, 'w', encoding='shift_jis', errors='ignore') as dest_file:
            dest_file.write(content)
        
        # 记录成功信息
        logging.info(f"File converted to Shift-JIS: {dest_path}")
    except Exception as e:
        # 如果转换过程中出现错误，记录错误信息
        logging.error(f"Error converting file to Shift-JIS {src_path}: {str(e)}")

# 处理单个文件
def process_file(file_path, output_folder):
    try:
        # 获取文件名（不包含扩展名）
        base_name = os.path.splitext(os.path.basename(file_path))[0]
        # 创建UTF-8 CSV文件路径
        csv_path = os.path.join(output_folder, f"{base_name}_utf8.csv")
        # 创建Shift-JIS CSV文件路径
        shiftjis_path = os.path.join(output_folder, f"{base_name}_shiftjis.csv")

        # 复制并重命名为CSV
        copy_and_rename(file_path, csv_path)
        
        # 转换为Shift-JIS
        convert_to_shift_jis(file_path, shiftjis_path)

    except Exception as e:
        # 如果处理过程中出现错误，记录错误信息
        logging.error(f"Error processing file {file_path}: {str(e)}")

# 主函数
def main():
    # 读取配置文件
    config = read_config()
    if not config:
        return

    # 从配置中获取输入文件夹路径
    input_folder_path = config['output_messagefolder']['path']
    # 从配置中获取输出文件夹路径
    output_folder_path = config['output_csvfolder']['path']
    # 从配置中获取日志文件夹路径，如果没有指定则使用默认值'logs'
    log_folder_path = config.get('log_folder', {}).get('path', 'logs')

    # 设置日志记录
    setup_logging(log_folder_path)

    # 创建输出文件夹（如果不存在）
    os.makedirs(output_folder_path, exist_ok=True)

    # 记录开始处理文件的信息
    logging.info(f"Starting processing of files in {input_folder_path}")

    # 遍历输入文件夹中的所有文件
    for file_name in os.listdir(input_folder_path):
        # 只处理.txt文件
        if file_name.endswith('.txt'):
            file_path = os.path.join(input_folder_path, file_name)
            # 处理单个文件
            process_file(file_path, output_folder_path)

    # 记录处理完成的信息
    logging.info("Processing complete")

# 如果这个脚本是直接运行的（而不是被导入的），则执行main函数
if __name__ == "__main__":
    main()