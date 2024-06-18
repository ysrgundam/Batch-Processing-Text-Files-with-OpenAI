import subprocess
import os

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
        "-a", app_id,
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

# 使用例
domain = 'arkconsulting.cybozu.com'
app_id = '64'
api_token = 'xlCFWsMbPjHcXtSHSX5soIbzuzCcFqrWcl0QmTBa'
csv_file_path = r'D:\00_WIP\07_AI_PowerAutomate\Code\extracted_data_utf8.csv'

print(repr(domain))
print(repr(app_id))
print(repr(api_token))
print(repr(csv_file_path))

# 関数を呼び出してデータをインポート
import_data_to_kintone(domain, app_id, api_token, csv_file_path)
