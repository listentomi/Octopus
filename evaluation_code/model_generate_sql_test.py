
from openai import OpenAI, RateLimitError
import os
import json
from tqdm import tqdm
import time
import datetime
import argparse
from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
)  # for exponential backoff

import re
from together import Together
import argparse


# os.environ["https_proxy"] = "http://localhost:7890"
gpt35_api_key = "your key"
gpt4_api_key = "your key"
gpt35_url = "https://api.chatanywhere.tech/v1"
proxy_url = 'https://api.openai-proxy.com'
# client = OpenAI(
#     # defaults to os.environ.get("OPENAI_API_KEY")
#     api_key=gpt4_api_key,
#     # base_url=gpt35_url
# )
client = Together(api_key='your key')


total_tokens_used = 0
prompt_tokens_used = 0
output_tokens_used = 0

@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def completion_with_backoff(**kwargs):
    return client.chat.completions.create(**kwargs)

def extract_list_objects(input_text):
    # 使用正则表达式匹配 SELECT 语句
    select_queries = re.findall(r'\bSELECT\b.*?;|\bWITH\b.*?;', input_text, re.DOTALL)
    return select_queries

def batch_generate_by_LLM(question_list=[],  create_table_sql="", model_choice="gpt-4-0125-preview"):
    messages = [
        {"role": "system", "content": f"Given the following SQL tables, your job is to write queries given a user’s request. \n\n{create_table_sql}"},
        {"role": "user","content": f'Write one SQL query end with ";" , for each question in the following question list:\n\n{question_list}\n\n'}
    ]

    completion = completion_with_backoff(model=model_choice, messages=messages,temperature=0.7, top_p=1)
    global total_tokens_used
    global prompt_tokens_used

    global output_tokens_used
    total_tokens_used+=completion.usage.total_tokens
    prompt_tokens_used+=completion.usage.prompt_tokens
    output_tokens_used+=completion.usage.completion_tokens
    print("one batch cost: ", completion.usage.total_tokens)
    response = completion.choices[0].message.content
    print(response)
    # print(extract_list_objects(response))
    if extract_list_objects(response) and len(extract_list_objects(response)) == len(question_list):
        return extract_list_objects(response)
    else:
        max_retry = 3
        retry_count = 0
        while not extract_list_objects(response):
            print("retrying...")
            if retry_count>max_retry:
                break
            completion = completion_with_backoff(model=model_choice, messages=messages,temperature=1, top_p=1)
            total_tokens_used+=completion.usage.total_tokens
            prompt_tokens_used+=completion.usage.prompt_tokens
            output_tokens_used+=completion.usage.completion_tokens
            print("one batch cost: ", completion.usage.total_tokens)
            response = completion.choices[0].message.content
            print(response)
            if extract_list_objects(response) and len(extract_list_objects(response)) == len(question_list):
                return extract_list_objects(response)
            retry_count+=1
        print("Failed to generate SQLs for this batch, please check the question list.")
        return question_list

def main():
    batch_size = 3
    parser = argparse.ArgumentParser(description='Model Generate SQL Test Together')
    parser.add_argument('--max_database_info_lines', type=int, default=1000, help='Maximum number of lines to read from database info file')
    parser.add_argument('--database_info_path', type=str, default='E:\A_final_benchmark\\test\\test_databases_create_info', help='Path to the database info file')
    parser.add_argument('--output_sql_path', type=str, default='E:\A_final_benchmark\\test\\test_generated_sqls_wizardLM_13b.json', help='Path to the output SQL file')
    parser.add_argument('--model_choice', type=str, default='WizardLM/WizardLM-13B-V1.2', help='Choice of the model')

    args = parser.parse_args()

    max_database_info_lines = args.max_database_info_lines
    database_info_path = args.database_info_path
    output_sql_path = args.output_sql_path
    model_choice = args.model_choice

    with open("E:\A_final_benchmark\\test\\test_filtered.json", "r",encoding='utf-8') as f:
        data = json.load(f)

    for db_name, db_entries in data.items():
        print(f"Database Name: {db_name}")
        current_db_question_list = []
        for entry in db_entries:
            current_db_question_list.append(entry['question'])
        # print(current_db_question_list)

        # 根据batch_size分批遍历问题列表
        with tqdm(total=len(current_db_question_list), desc="Generating SQLs") as pbar:
            for i in range(0, len(current_db_question_list), batch_size):
                batch_question_list = current_db_question_list[i:i+batch_size]
                pbar.update(len(batch_question_list))
                # 以字符串形式读取指定路径的.sql文件
                with open(os.path.join(database_info_path,f"{db_name}_create.sql"), "r") as f:
                    create_table_sql = f.readlines()[:max_database_info_lines]
                
                batch_generated_SQLs_list=batch_generate_by_LLM(batch_question_list, create_table_sql,model_choice=model_choice)
                # 将batch_generated_SQLs_list的元素添加到generated_SQLs_list中
                if batch_generated_SQLs_list:
                    for sql in batch_generated_SQLs_list:
                        if not os.path.exists(output_sql_path):
                            with open(output_sql_path, 'w', encoding='utf-8') as f:
                                json.dump([{db_name:sql}],f,ensure_ascii=False,indent=4)
                        # 如果output_sql_path文件存在，则将json对象列表续写入文件
                        else:
                            with open(output_sql_path, 'r', encoding='utf-8') as f:
                                data = json.load(f)
                            data.append({db_name:sql})
                            with open(output_sql_path, 'w', encoding='utf-8') as f:
                                json.dump(data,f,ensure_ascii=False,indent=4)
                time.sleep(1)
    return 

if __name__=='__main__':

    main()