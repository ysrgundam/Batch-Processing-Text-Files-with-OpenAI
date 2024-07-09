import subprocess
import os
import yaml

def import_data_to_kintone(domain, app_id, api_token, csv_file_path):
    """
    KintoneのアプリにCSVファイルを用いてデータをインポートする。
    :param domain: kintoneのドメイン名
    :param app_id: アプリID
    :param api_token: APIトークン
    :param csv_file_path: インポートするCSVファイルのパス
    :return: インポートが成功したかどうかを示すブール値
    """
    cli_command = [
        "cli-kintone.exe",
        "--import",
        "-d", domain,
        "-a", str(app_id),
        "-t", api_token,
        "-f", csv_file_path,
        "-e", "utf-8"
    ]
    try:
        result = subprocess.run(cli_command, check=True, capture_output=True, text=True, encoding='utf-8')
        print("データのインポートに成功しました:")
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print("データのインポートに失敗しました:")
        print(e.output)
        return False

# Config.yamlファイルを読み込む
with open('config.yaml', 'r', encoding='utf-8') as file:
    config = yaml.safe_load(file)

# Config.yamlファイルから値を取得する
domain = config['kintone']['domain']
app_id = config['kintone']['app_id']
api_token = config['kintone']['api_token']
output_folder_path = config['output_csvfolder']['path']

# UTF-8エンコードのCSVファイルを見つける
csv_files = [f for f in os.listdir(output_folder_path) if f.endswith('_utf8.csv')]

successful_imports = 0
total_files = len(csv_files)

if csv_files:
    for csv_file_name in csv_files:
        csv_file_path = os.path.join(output_folder_path, csv_file_name)
        print(f"処理中のファイル: {csv_file_name}")
        print(repr(domain))
        print(repr(app_id))
        print(repr(api_token))
        print(repr(csv_file_path))
        # 関数を呼び出してデータをインポート
        if import_data_to_kintone(domain, app_id, api_token, csv_file_path):
            successful_imports += 1
else:
    print("UTF-8エンコードのCSVファイルが見つかりませんでした。")

print(f"\n処理完了: 合計{total_files}件中{successful_imports}件のファイルが正常にアップロードされました。")