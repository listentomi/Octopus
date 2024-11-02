import requests
import openai

OPENAI_API_KEY="YOUR_API_KEY"
url = "https://api.chatanywhere.tech/v1"
headers = {
    "Authorization": f"Bearer {OPENAI_API_KEY}"
}
payload = {
    "purpose": "fine-tune",
}
output_file_path = r'./data/SQL_data.txt'
print('数据路径: ', output_file_path)
files = {
    "file": open(output_file_path, "rb")
}

response = requests.post(url, headers=headers, data=payload, files=files)
print(response)
# 单独调用 openai.File方法查询已上传文件信息
print('上传的文件信息: ', openai.File.list())