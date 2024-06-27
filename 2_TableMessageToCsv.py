import os
import yaml
import pandas as pd
from io import StringIO
import re
import csv
import codecs
import logging
from datetime import datetime
import traceback

def setup_logging(log_folder):
    os.makedirs(log_folder, exist_ok=True)
    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = os.path.join(log_folder, f"markdown_to_csv_{current_time}.log")
    
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
        logging.error(f"Error reading config file: {str(e)}\n{traceback.format_exc()}")
        return None

def preprocess_table_content(content):
    pattern = r"\|提供元案件番号\|.*?(?=\n\n|\Z)"
    table_content = re.search(pattern, content, re.DOTALL)
    
    if not table_content:
        raise ValueError("No table content found in the file")
    
    return table_content.group(0)

def convert_to_dataframe(table_content):
    data_io = StringIO(table_content)
    try:
        df = pd.read_csv(data_io, sep='|', skipinitialspace=True)
        df.columns = df.columns.str.strip()
        df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
        return df
    except pd.errors.ParserError as e:
        logging.error(f"ParserError: {str(e)}\n{traceback.format_exc()}")
        logging.error(f"Problematic content:\n{table_content}")
        return None

def save_csv(df, output_path, encoding='utf-8'):
    try:
        df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
        df.to_csv(output_path, index=False, encoding=encoding, quoting=csv.QUOTE_ALL)
        logging.info(f"CSV saved successfully: {output_path}")
    except UnicodeEncodeError as e:
        logging.error(f"UnicodeEncodeError: {str(e)}\nProblematic data:\n{df[df.applymap(lambda x: '\uFFFD' in str(x))]}")
    except Exception as e:
        logging.error(f"Error saving CSV: {str(e)}\n{traceback.format_exc()}")

def read_csv(file_path, encoding='utf-8'):
    try:
        df = pd.read_csv(file_path, encoding='utf-8-sig', index_col=False)
        df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
        return df
    except Exception as e:
        logging.error(f"Error reading CSV: {str(e)}\n{traceback.format_exc()}")
        return None

def convert_encoding(input_path, output_path, input_encoding='utf-8', output_encoding='shift_jis'):
    try:
        df = read_csv(input_path, input_encoding)
        if df is not None:
            logging.debug(f"DataFrame shape before conversion: {df.shape}")
            logging.debug(f"DataFrame columns: {df.columns}")
            logging.debug(f"First few rows:\n{df.head()}")
            
            df_encoded = df.applymap(lambda x: str(x).encode(output_encoding, errors='ignore').decode(output_encoding))
            
            df_encoded.to_csv(output_path, index=False, encoding=output_encoding, quoting=csv.QUOTE_ALL)
            
            logging.info(f"Encoding conversion complete. Output file: {output_path}")
            logging.debug(f"DataFrame shape after conversion: {df_encoded.shape}")
        else:
            logging.error(f"Failed to read input file: {input_path}")
    except Exception as e:
        logging.error(f"Error during encoding conversion: {str(e)}\n{traceback.format_exc()}")

def process_file(file_path, output_folder):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            email_content = file.read()

        logging.info(f"Processing file: {file_path}")
        
        table_content = preprocess_table_content(email_content)
        df = convert_to_dataframe(table_content)

        if df is not None and not df.empty:
            base_name = os.path.splitext(os.path.basename(file_path))[0]
            utf8_path = os.path.join(output_folder, f"extracted_data_utf-8_{base_name}.csv")
            shiftjis_path = os.path.join(output_folder, f"extracted_data_shiftjis_{base_name}.csv")

            save_csv(df, utf8_path, 'utf-8')
            convert_encoding(utf8_path, shiftjis_path)
        else:
            logging.error(f"Failed to create DataFrame or DataFrame is empty for file: {file_path}")

    except Exception as e:
        logging.error(f"Error processing file {file_path}: {str(e)}\n{traceback.format_exc()}")

def check_csv_content(file_path, encoding):
    try:
        with open(file_path, 'r', encoding=encoding) as f:
            content = f.read()
            logging.info(f"Content of {file_path} ({encoding}):")
            logging.info(content[:500])  # 只记录前500个字符
    except Exception as e:
        logging.error(f"Error reading {file_path}: {str(e)}")

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
            
            base_name = os.path.splitext(file_name)[0]
            utf8_path = os.path.join(output_folder_path, f"extracted_data_utf-8_{base_name}.csv")
            shiftjis_path = os.path.join(output_folder_path, f"extracted_data_shiftjis_{base_name}.csv")
            
            check_csv_content(utf8_path, 'UTF-8')
            check_csv_content(shiftjis_path, 'shift_jis')

    logging.info("Processing complete")

if __name__ == "__main__":
    main()