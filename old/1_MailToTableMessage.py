from openai import OpenAI

# 初始化OpenAI客户端
client = OpenAI(api_key='KLmy1EtC4jRcrlXSK2xPgesG5Hgc533A', base_url='http://Bedroc-Proxy-THtYZpmCMIzd-1859376833.us-east-1.elb.amazonaws.com/api/v1')

# 读取本地文件
file_path = 'D:\\00_WIP\\07_AI_PowerAutomate\\Code\\TestFile.txt'
with open(file_path, 'r', encoding='utf-8') as file:
    email_content = file.read()

# 构建完整的prompt
prompt_text = f"""
下記のメールはITプロジェクト参加するメンバーの募集案件案件です。
募集案件を表形式で以下の項目情報を抽出してください。
メール内複数件案件含まれていることがあるため、各案件を別々の行にして出力してください。
表の各列は以下の項目に対応させてください。それ以外一切話しないでください。

# 項目一覧
紹介日: メールの受信日（フォマードはYYYY/MM/DD）
提供元案件番号: メールで記載された案件番号
委託元: 案件の依頼主、あるいば提案先
業界: 案件クライアントの業界
PJフェーズ: 案件はPJのフェーズ
モジュール: SAP案件の場合、SAPのモジュール
SAP案件：〇と×で判断
単価：万円/月
募集人数：案件募集の人数
開始日：募集する方のアサイン日
終了日：募集する方のリリース日
勤務地
案件概要：案件内容のまとめ
必須要件（経験・スキル）：必須の項目を記載
歓迎要件（経験・スキル）：望ましい・関係の項目を記載
言語力：日本語、英語、中国語など
メインポジション：リーダー、PMO、作業者など

# メール
{email_content}

# 希望の表形式出力例
紹介日|提供元案件番号|委託元|業界|PJフェーズ|モジュール|SAP案件|単価|募集人数|開始日|終了日|勤務地|案件概要|必須要件|歓迎要件|言語力|メインポジション
2024/4/26|AB-263|Accenture|電力|設計フェーズ|CO|〇|100万円程度|1|即日|2024/6/30|江東区/木場 週3回出社+リモート|SAP S4HANA導入（会計のみ）|"FIモジュール標準機能の基本設計、カスタマイズ定義 資金管理もしくは伝票決算業務について、GL|AP|ARを横断的にカスタマイズする。"|SAP S4HANA FIモジュールの標準機能理解 基本設計書作成経験|電力事業案件の経験（会計領域が望ましい）|日本語|アプリ設計
2024/4/26|AF-269|Accenture|大手メーカー| |Dinamics365|×|100万円程度|1|要確認|要確認|リモート(今後汐留・赤坂への出社可能性)|Dinamics365の導入（要件定義リリース）障害対応、テスト後エラー修正、改修業務、CR対応|要件定義からはじめるケースもあり。|Dinamics365の導入経験（要件定義リリース） 会計もしくはロジ物流 の業務知識 X++でのアプリ基本設計経験（開発尚可） |Dinamics365|日本語|アプリ設計
"""

# 设置最大token数
max_tokens = 4096  # 例如，限制为150个token，根据需要调整

# 创建聊天完成请求，加入max_tokens参数
completion = client.chat.completions.create(
    model="anthropic.claude-3-haiku-20240307-v1:0",
    messages=[{"role": "user", "content": prompt_text}],
    max_tokens=max_tokens  # 设置输出的最大token数
)

# 获取模型的输出并存储到变量
model_output = completion.choices[0].message.content

# 现在 model_output 变量包含了模型的输出
print(model_output)

# 打开一个文件进行写入
with open('MessageFile.txt', 'w', encoding='utf-8') as file:
    file.write(model_output)

# 打印一条信息确认文件已被保存
print("Output saved to MessageFile.txt")