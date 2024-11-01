
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
from together import Together

# os.environ["https_proxy"] = "http://localhost:10809"
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
    # return client.completions.create(**kwargs)

# 编写函数提取输入字符串中可能存在的列表对象
def extract_list_objects(input_string):
    # 从输入字符串中提取可能存在的列表对象
    list_objects = []
    # 从输入字符串中提取可能存在的列表对象
    
    for i in range(len(input_string)):
        if input_string[i] == '[':
            start = i
        if input_string[i] == ']':
            end = i
            try:
                list_objects.append(eval(input_string[start:end+1]))
            except:
                pass
    if len(list_objects) == 0:
        return None
    return list_objects[0]

def batch_generate_by_LLM(question_list=[],  ext_know_list = [], create_table_sql="", model_choice="gpt-4-0125-preview"):

    example_question_list  = ["List all loan applicants' IDs, income, and loan amounts, and calculate their income-to-debt ratio. Sort by income-to-debt ratio in descending order."]
    example_answer_list = ["SELECT \n  SK_ID_CURR AS ID, \n  AMT_INCOME_TOTAL AS Income, \n  AMT_CREDIT AS Loan_Amount, \n  AMT_CREDIT/AMT_INCOME_TOTAL AS Debt_Income_Ratio\nFROM \n  application_train\nORDER BY \n  Debt_Income_Ratio DESC;"] 
    messages = [
        {"role": "system", "content": f"Given the following SQL tables, your job is to write queries given a user’s request. \n\n{create_table_sql}"},
        {"role": "user","content": f'Write a SQL query for each question in the following question list:\n\n{example_question_list}\n\n External knowledge: {ext_know_list}\n\nOnly print the generated SQLs in a list object formatted as \n\n["generated_sql1","generated_sql2","generated_sql3",...].'},
        {"role": "assistant", "content": f"{example_answer_list}"},
        {"role": "user","content": f'Write a SQL query for each question in the following question list:\n\n{question_list}\n\n External knowledge: {ext_know_list}\n\nOnly print the generated SQLs in a list object formatted as \n\n["generated_sql1","generated_sql2","generated_sql3",...].'},
    ]
    completion = completion_with_backoff(model=model_choice, messages=messages,temperature=1, top_p=1)
    global total_tokens_used
    global prompt_tokens_used

    global output_tokens_used
    total_tokens_used+=completion.usage.total_tokens
    prompt_tokens_used+=completion.usage.prompt_tokens
    output_tokens_used+=completion.usage.completion_tokens
    print("one batch cost: ", completion.usage.total_tokens)
    response = completion.choices[0].message.content
    if extract_list_objects(response) and len(extract_list_objects(response))==len(question_list):
        return extract_list_objects(response)
    else:
        max_retry = 5
        retry_count = 0
        while (not extract_list_objects(response)) or len(extract_list_objects(response))<len(question_list):
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
            if extract_list_objects(response) and len(extract_list_objects(response))==len(question_list):
                return extract_list_objects(response)
            retry_count+=1
        print("Failed to generate SQLs for this batch, please check the question list.")
        return question_list

def main():
    batch_size = 1

    database_info_path = '.\\test\\test_databases_create_info'
    output_sql_path = '.\\test\\test_generated_sqls_codellama_34b_ext_w.json'
    
    with open(".\\test\\test_external_knowledge_for_generative.json", "r",encoding='utf-8') as f:
        data = json.load(f)

    for db_name, db_entries in data.items():
        print(f"Database Name: {db_name}")
        current_db_question_list = []
        ext_know_list = []
        for entry in db_entries:
            current_db_question_list.append(entry['question'])
            ext_know_list.append(entry['ext knowledge'])
        # print(current_db_question_list)

        # 根据batch_size分批遍历问题列表
        with tqdm(total=len(current_db_question_list), desc="Generating SQLs") as pbar:
            for i in range(0, len(current_db_question_list), batch_size):
                batch_question_list = current_db_question_list[i:i+batch_size]
                batch_ext_list = ext_know_list[i:i+batch_size]
                pbar.update(len(batch_question_list))
                # 以字符串形式读取指定路径的.sql文件
                with open(os.path.join(database_info_path,f"{db_name}_create.sql"), "r") as f:
                    create_table_sql = f.read()
                batch_generated_SQLs_list=batch_generate_by_LLM(batch_question_list, batch_ext_list, create_table_sql,model_choice='codellama/CodeLlama-34b-Instruct-hf')
                # 将batch_generated_SQLs_list的元素添加到generated_SQLs_list中
                if batch_generated_SQLs_list:
                    for sql,ext_k in zip(batch_generated_SQLs_list,batch_ext_list):
                        if not os.path.exists(output_sql_path):
                            with open(output_sql_path, 'w', encoding='utf-8') as f:
                                json.dump([{db_name:sql,"ext_k":ext_k}],f,ensure_ascii=False,indent=4)
                        # 如果output_sql_path文件存在，则将json对象列表续写入文件
                        else:
                            with open(output_sql_path, 'r', encoding='utf-8') as f:
                                data = json.load(f)
                            data.append({db_name:sql,"ext_k":ext_k})
                            with open(output_sql_path, 'w', encoding='utf-8') as f:
                                json.dump(data,f,ensure_ascii=False,indent=4)
                time.sleep(1)
    return 

if __name__=='__main__':
    main()