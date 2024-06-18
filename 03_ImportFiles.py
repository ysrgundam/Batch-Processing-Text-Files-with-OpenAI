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
    """
    # CLIコマンドを構築
    cli_command = [
        "cli-kintone.exe",  # CLIツールのパスを適宜修正してください
        "--import",
        "-d", domain,
        "-a", str(app_id),
        "-t", api_token,
        "-f", csv_file_path,
        "-e", "utf-8"
    ]
    # コマンドを実行
    try:
        result = subprocess.run(cli_command, check=True, capture_output=True, text=True, encoding='utf-8')
        print("データのインポートに成功しました:")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print("データのインポートに失敗しました:")
        print(e.output)

# Config.yamlファイルを読み込む
with open('config.yaml', 'r', encoding='utf-8') as file:
    config = yaml.safe_load(file)

# Config.yamlファイルから値を取得する
domain = config['kintone']['domain']
app_id = config['kintone']['app_id']
api_token = config['kintone']['api_token']
output_folder_path = config['output_csvfolder']['path']

# UTF-8エンコードのCSVファイルを見つける
csv_file_name = None
for file_name in os.listdir(output_folder_path):
    if file_name.startswith('extracted_data_utf-8_') and file_name.endswith('.csv'):
        csv_file_name = file_name
        break

if csv_file_name:
    csv_file_path = os.path.join(output_folder_path, csv_file_name)
    print(repr(domain))
    print(repr(app_id))
    print(repr(api_token))
    print(repr(csv_file_path))
    # 関数を呼び出してデータをインポート
    import_data_to_kintone(domain, app_id, api_token, csv_file_path)
else:
    print("UTF-8エンコードのCSVファイルが見つかりませんでした。")