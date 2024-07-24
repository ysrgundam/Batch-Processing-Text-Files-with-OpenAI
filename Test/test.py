import subprocess
import os
import yaml

cli_command = [
    "cli-kintone.exe",  # Kintone命令行工具
    "--export",  # 导入操作
    "-d", "arkconsulting.cybozu.com",  # 指定域名
    "-a", str("45"),  # 指定应用ID
    "-t", "MjAfB7x6uFg0UvhvG9bsUWOMXKRxYDqSQQgZC3ZU",  # 指定API令牌
]
result = subprocess.run(cli_command, check=True, capture_output=True, text=True, encoding='utf-8')
print(result.stdout)