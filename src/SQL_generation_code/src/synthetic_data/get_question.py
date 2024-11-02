# import openai
# import json

# # 创建一个 OpenAI 客户端
# client = openai.OpenAI(
#     api_key="sk-KIuv9VzNDqsC4otPqo4m9IUqCUnnVAvn7SuNQqLMouA5TGy0",
#     base_url="https://api.chatanywhere.tech/v1"
# )

# input_question = "What does the table contain?"
# # 创建 'messages' 列表，其中包含 'sql' 和 'question'
# messages = [
#     {"role": "system", "content": "I will provide you with English text, please translate it into reasonable and fluent Chinese."},
#     {"role": "user", "content": input_question},
#     {"role": "user", "content": "Translate the above into Chinese."},
# ]
# # 调用 GPT API
# response = client.chat.completions.create(model="gpt-3.5-turbo", messages=messages, n=2)
# # 打印响应内容
# print(response.choices[0].message.content)
import json
import pandas as pd
import openai
# 读取JSON文件
client = openai.OpenAI(
    api_key="YOUR_API_KEY",
    base_url="https://api.chatanywhere.tech/v1"
)
with open('C:\\Users\\86130\\Downloads\\sql\\results\\results\\new_airline.json', 'r') as f:
    data = json.load(f)
# 将数据转换为pandas DataFrame
df = pd.DataFrame(data)
# 对于每个 'question'，进行翻译
for index, row in df.iterrows():
    input_question = row['question']
    messages = [
        {"role": "system", "content": "I will provide you with English text, please translate it into reasonable and fluent Chinese."},
        {"role": "user", "content": input_question},
        {"role": "user", "content": "Translate the above into Chinese."},
    ]
    # 调用 GPT API
    response = client.chat.completions.create(model="gpt-3.5-turbo", messages=messages, n=2)
    # 添加翻译结果到 'chinese-question' 列
    df.loc[index, 'chinese-question'] = response.choices[0].message.content
    translation = translation.replace('独特', '不重复')
    print(response.choices[0].message.content)
# 保存新的DataFrame为JSON文件
data_dict = df.to_dict('records')
# 保存字典列表为JSON文件
with open('C:\\Users\\86130\\Downloads\\sql\\results\\results\\airline_questions.json', 'w', encoding='utf-8') as f:
    json.dump(data_dict, f, ensure_ascii=False, indent=2)
