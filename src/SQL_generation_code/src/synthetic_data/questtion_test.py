from openai import OpenAI
import json
import pandas as pd
import csv
import re

client = OpenAI(
    # defaults to os.environ.get("OPENAI_API_KEY")
    api_key="YOUR_API_KEY",
    base_url="https://api.chatanywhere.tech/v1"
)

csv_file_path = r'C:\Users\86130\Downloads\sql\data\power\generative\question.csv'
df = pd.read_csv(csv_file_path, header=None, usecols=[0], encoding='gbk')

# 将第一列的数据转为列表
queries = df[0].tolist()

# 非流式响应
def gpt_35_api(messages: list):
    completion = client.chat.completions.create(model="gpt-3.5-turbo", messages=messages, n=2)
    #print(completion.choices[0].message.content)
    return completion.choices[0].message.content, completion.choices[1].message.content

file_path = r'C:\Users\86130\Downloads\电力\output.txt'
with open(file_path, 'r', encoding='utf-8') as file:
    string = file.read()


sample = "SELECT count(*) FROM c_cons_prc_tactic AS T1"
def generate_question(sql_statement):
    prompt = f"""
    We know {string}.
    Given the following SQL statement:

    ```sql
    {sql_statement}
    ```

    Please generate a question (in Chinese) that can be answered using the given SQL statement.
    """
    return prompt

# messages = [{'role': 'user','content': generate_question(sample)}]
# message, m= gpt_35_api(messages)
# print(message)
# print("*****")
# print(m)

# def change_message(message):
#     words = message.split()
#     message = " ".join(words[-1:])
#     matches = re.findall(r'"([^"]*)"', message)
#     # 如果找到匹配项，选取第一个匹配项
#     result = matches[0] if matches else message
#     return result

csv_file_path = r"C:\Users\86130\Downloads\sql\data\power\generative\generate_question.csv"
with open(csv_file_path, "a", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Sample", "Message1", "Message2"])  # 写入标题行
    # 循环处理每个 sample
    for sample in queries:
        messages = [{'role': 'user','content': generate_question(sample)}]
        message1, message2 = gpt_35_api(messages)
        # message1 = change_message(message1)
        # message2 = change_message(message2)
        # 写入当前 sample 和 message
        writer.writerow([sample, message1, message2])
        print(message1)
        print("********")
        print(message2)