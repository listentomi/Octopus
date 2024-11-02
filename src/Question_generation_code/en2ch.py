import argparse
import time
import json
from openai import APIConnectionError, OpenAI
from progress.bar import Bar
import concurrent.futures
import random
import yaml
from src.qa import makecomversation

# 读取配置文件，拿到openai的api key
def load_config(file_path):
    with open(file_path, 'r') as config_file:
        config = yaml.safe_load(config_file)
    return config

config = load_config('config.yaml')

client = OpenAI(
    api_key=config['api']['key']
)


# 让gpt分析下句子中的名词
def getExplanations(en):
     
    def say(prompt, usercontent, return_format, temperature=0):
        def sendquestion(prompt, usercontent):
            message = [
                    {
                        "role": "system",
                        "content": prompt
                    },
                    {
                        "role": "user",  
                        "content": usercontent 
                    }
                ]
            
            chat_completion = client.chat.completions.create(
                model="gpt-3.5-turbo-1106",
                # model="gpt-4-1106-preview",
                messages=message,
                temperature=temperature,
                # response_format={"type": "json_object"}
                )
            return chat_completion
        try:
          chat_completion = sendquestion(prompt, usercontent)
        except Exception as e: 
          chat_completion = sendquestion(prompt, usercontent)
          
        answer = chat_completion.choices[0].message.content
        return answer

    prompt = f""" 请用中文回答问题.
    """

    usercontent = f""" 
    {en}\n 请你分析其中涉及的名词的含义.
    """

    return_format = '{"answer":"your answer to the question"}'

    result = say(prompt, usercontent, return_format)
  
    return result


# random fewshot 翻译
def getAnswer(en, explanations):

    with open('./CSpider/en2ch_examples.json', 'r', encoding='utf-8') as f:
        spider_examples = json.load(f)
    random_selection = random.sample(spider_examples, 10)

    examples = ''
    index = 1
    for item in random_selection:
        example = f"examples{index}: \"{item['english question']}\", its Chinese translation is \"{item['chinese question']}\".\n"
        examples += example
        index += 1

    prompt = f"""You are a translation expert. You need to translated the english question to chinese question. 
    当你看到单词unique例如'unique ticket numbers'，它通常是"不同的"意思， 例如
    "for each unique aircraft code" 可以翻译为"每个不同的飞机代码" 而不是"每个独特的飞机代码"。
    here are some examples:
    {examples}
    """

    usercontent = f""" Translate the chinese question provided below, then return the translated english question.
    The english question is: {en} 
    Here is some explanations about the english question to help you understand it better:
    {explanations}
    """

    return_format = '{"chinese result":"the chinese translation of provided english question"}'

    result = makecomversation(prompt, usercontent, return_format, client)
  
    return result['chinese result']

# 翻译主函数
def en2ch(en):
    explanations = getExplanations(en)
    ch = getAnswer(en, explanations)
    return ch


if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description='english to chinese question translation')

    # random seed
    parser.add_argument('--sql_path', type=str, default='salika_sqls.txt', help='输入文件')
    parser.add_argument('--output_path', type=str, default='new_salika.txt', help='结果输出文件')

    args = parser.parse_args()

    sql_path = args.sql_path
    output_path = args.output_path
    start_time = time.time()


    filetype = str(sql_path).split('.')[-1]

    
    with open(sql_path, 'r') as file:
        if filetype == 'json':
            jsonfile = json.load(file)
            english_question = []
            for item in jsonfile:
                english_question.append(item['question'])
        else:
            english_question = file.readlines()
    

    total_number  = len(english_question)
    
    print("read sqls successfully!, total number of sqls: ", total_number, "\n\n")
    

    
    en_ch_pairs = []
    bar = Bar(f'{sql_path}:', max=total_number)
    err_list = []
    
    # 多线程翻译
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_sentence = {executor.submit(en2ch, en): en for en in english_question}
        
        for future in concurrent.futures.as_completed(future_to_sentence):
            en = future_to_sentence[future]
            bar.next()
            try:
                ch = future.result()
                en_ch_pairs.append({'en': en, 'ch': ch})
            except Exception as e:
                print("翻译句子",en,"时出现异常:", e)
                err_list.append(en)


    end_time = time.time()  
    total_time = end_time - start_time
    print(f"generate question for {sql_path} finishied. {len(err_list)} total time cost {total_time} seconds\n\n")

    
    with open(output_path, 'w', encoding="utf-8") as file:
        if filetype == 'json':
            jsonresults = []
            # 找到json item的英文问题和en_ch_pairs的英文问题对应
            for item in jsonfile:
                for en_ch_pair in en_ch_pairs:
                    if item['question'] == en_ch_pair['en']:
                        item['chinese question'] = en_ch_pair['ch']
                        jsonresults.append(item)
                        break
            json.dump(jsonresults, file, indent=4, ensure_ascii=False)
        else:
            for item in en_ch_pairs:
                file.write(f"{item['en']}\n{item['ch']}\n\n")
    print(f"file write to {output_path}\n\n")