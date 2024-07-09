import os
import shutil
import yaml
import logging
from datetime import datetime

def setup_logging(log_folder):
    os.makedirs(log_folder, exist_ok=True)
    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = os.path.join(log_folder, f"file_converter_{current_time}.log")
    
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler()
        ]
    )
    
    logging.info(f"Log file created at: {log_file}")

def read_config(config_path='config.yaml'):
    try:
        with open(config_path, 'r', encoding='utf-8') as file:
            return yaml.safe_load(file)
    except Exception as e:
        logging.error(f"Error reading config file: {str(e)}")
        return None

def copy_and_rename(src_path, dest_path):
    try:
        shutil.copy2(src_path, dest_path)
        logging.info(f"File copied and renamed: {dest_path}")
    except Exception as e:
        logging.error(f"Error copying file {src_path}: {str(e)}")

def convert_to_shift_jis(src_path, dest_path):
    try:
        with open(src_path, 'r', encoding='utf-8') as src_file:
            content = src_file.read()
        
        with open(dest_path, 'w', encoding='shift_jis', errors='ignore') as dest_file:
            dest_file.write(content)
        
        logging.info(f"File converted to Shift-JIS: {dest_path}")
    except Exception as e:
        logging.error(f"Error converting file to Shift-JIS {src_path}: {str(e)}")

def process_file(file_path, output_folder):
    try:
        base_name = os.path.splitext(os.path.basename(file_path))[0]
        csv_path = os.path.join(output_folder, f"{base_name}_utf8.csv")
        shiftjis_path = os.path.join(output_folder, f"{base_name}_shiftjis.csv")

        # 复制并重命名为CSV
        copy_and_rename(file_path, csv_path)
        
        # 转换为Shift-JIS
        convert_to_shift_jis(file_path, shiftjis_path)

    except Exception as e:
        logging.error(f"Error processing file {file_path}: {str(e)}")

def main():
    config = read_config()
    if not config:
        return

    input_folder_path = config['output_messagefolder']['path']
    output_folder_path = config['output_csvfolder']['path']
    log_folder_path = config.get('log_folder', {}).get('path', 'logs')

    setup_logging(log_folder_path)

    os.makedirs(output_folder_path, exist_ok=True)

    logging.info(f"Starting processing of files in {input_folder_path}")

    for file_name in os.listdir(input_folder_path):
        if file_name.endswith('.txt'):
            file_path = os.path.join(input_folder_path, file_name)
            process_file(file_path, output_folder_path)

    logging.info("Processing complete")

if __name__ == "__main__":
    main()