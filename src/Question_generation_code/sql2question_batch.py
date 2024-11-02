import argparse
import time
import json
from openai import APIConnectionError, OpenAI
from progress.bar import Bar
import concurrent.futures
import re
import sqlparse
from sqlparse.sql import IdentifierList, Identifier, Where
import sqlparse.tokens as Token
# import mysql.connector


from src.qa import makecomversation
from src.decomp import get_clause, after_process
import os
import pandas as pd
import math
remove_aliases_input = 0
remove_aliases_output = 0

place_tablename_input = 0
place_tablename_output = 0

rough_tranlate_clause_input = 0
rough_tranlate_clause_output = 0

fewshot_tranlate_clause_input = 0
fewshot_tranlate_clause_output = 0

the_final_translate_input = 0
the_final_translate_output = 0

en2ch_input = 0
en2ch_output = 0

# 取消别名 300 token
def remove_aliases(sqls):
    inputs = {}
    for i, sql in enumerate(sqls):
        inputs[f'sql{i+1}'] = sql 
    prompt = """You are a SQL parsing expert. You need to remove the aliases in sql statement, then return the SQL statement without the aliases. Here is one examples:
    WITH clause is not considered in this task.
    before:
          "SELECT DISTINCT count(anon_1.c_4200) OVER (PARTITION BY anon_1.description) AS c_4528, 
          anon_1.c_141, 
          anon_1.description 
          FROM (
            SELECT film_text.description AS description, 
            count(distinct(film_text.film_id)) AS c_141, 
            count(film_text.title) OVER (ORDER BY film_text.title) AS c_4200 
            FROM film_text 
            WHERE (film_text.film_id >= %(film_id_1)s) 
            GROUP BY film_text.title, film_text.description, film_text.film_id) AS anon_1
    after: 
          SELECT DISTINCT COUNT(film_text.title) OVER (PARTITION BY film_text.description), 
                COUNT(DISTINCT film_text.film_id) 
                film_text.description
          FROM (
              SELECT film_text.description, 
                    COUNT(DISTINCT film_text.film_id) , 
                    COUNT(film_text.title) OVER (ORDER BY film_text.title)
              FROM film_text
              WHERE film_text.film_id >= %(film_id_1)s
              GROUP BY film_text.title, film_text.description, film_text.film_id
          ) ;
    """

    usercontent = f""" You need to remove the aliases from the SQL provided below, then return the SQL statement without the aliases.
    Make sure you return a valid SQL statement, do not generate any other content, it you find problem in sql provided, ignore it.  

    The SQL statements are: 
    {inputs}
    """

    return_format = '{"sql1":"","sql1":"",...}'

    result, input_tokens, ouput_tokens = makecomversation(prompt, usercontent, return_format)
    global remove_aliases_input
    global remove_aliases_output
    remove_aliases_input += input_tokens
    remove_aliases_output += ouput_tokens
    result1 = []
    for i, sql in enumerate(sqls): 
        result1.append(result[f'sql{i+1}'])
    return result1, input_tokens, ouput_tokens


# 添加表名 200token
def place_tablename(sqls):
    inputs = {}
    for i, sql in enumerate(sqls):
        inputs[f'sql{i+1}'] = sql


    prompt = """You are a SQL parsing expert. You need to add the table name to all the indicator that appear in the sql statement. """

    usercontent = f""" 
        You need to add the table name to all the indicator that appear in the sql statement。
        Make sure there are no omissions. 
        Do not abbreviate the table name. 
        if the table is is already correctly formatted return the original SQL statement.

        The SQL statements are: 
        {inputs}
        """
    
    return_format = '{"sql1":"","sql2":"",...}'

    result, input_tokens, ouput_tokens = makecomversation(prompt, usercontent, return_format)
    global place_tablename_input
    global place_tablename_output
    place_tablename_input += input_tokens
    place_tablename_output += ouput_tokens
    result1 = []
    for i, sql in enumerate(sqls):
        result1.append(result[f'sql{i+1}'])
    return result1, input_tokens, ouput_tokens

# 替换运算符
def replace_logical_operators(sql):
    WHERE_OPS = ('not', 'between', '=', '>', '<', '>=', '<=', '!=', 'in', 'like', 'is', 'exists')
    WHERE_OPS_NL = ('not', 'between', 'equal to', 'more than', 'less than', 'no less than', 'no more than', 'not equal to', 'in', 'like', 'is', 'exists')
    for op, nl in zip(WHERE_OPS, WHERE_OPS_NL):
                            op_str = f" {op} "
                            if  op_str in sql:
                                sql = sql.replace(op_str, f" {nl} ")
                            
    return sql

#### 预处理：

def preprocess(sqls, jump=True):
    inputs1 = 0
    outputs1 = 0
    inputs2 = 0
    outputs2 = 0

    if not jump:    
        sqls, inputs1, outputs1 = remove_aliases(sqls)  
        sqls, inputs2, outputs2 = place_tablename(sqls)

    results = []
    for sql in sqls:
        sql = replace_logical_operators(sql)
        results.append(sql)
    
    return results, inputs1, inputs2, outputs1, outputs2

# 提取sql相关字段
def get_indicators(clause_list):
  pattern = r'\b\w+\.\w+\b'
  sql_indicators = []
  for clause in clause_list:
    matches = re.findall(pattern, clause)
    sql_indicators += matches
  return sql_indicators # [table.column, table.column, ...]


# 获取字段描述
def get_sql_descriptions(cluse_list, db_name = None):
    if db_name is None:
        return None
    
    des_path = f'./database_descriptions/{db_name}_descriptions.csv'

    if not os.path.exists(des_path):
        return None
    
    descriptions = pd.read_csv(des_path)


    indicators = get_indicators(cluse_list)

    relevent_descriptions = []
    for indicator in indicators:
        table, column = indicator.split('.')
        print(table, column)
        try:   
            print(descriptions[(descriptions['table'] == table) & (descriptions['column'] == column)]['description'])
            descirption = descriptions[(descriptions['table'] == table) & (descriptions['column'] == column)]['description'].values[0]
            relevent_descriptions.append(f'column {column} in table {table} is {descirption}. ')
        except KeyError:
            pass

    return relevent_descriptions
        

# 粗翻译,翻译到接近自然语言,没有特殊标记符号,和类似函数的表达形式.  200 tokens
def rough_tranlate_clause(sentences):
    prompt = """You are a Translator."""

    usercontent = f""" 
    Translate the sentences provided into spoken English, not contain any special symbols except commas and periods.
    Only returns the translated sentences, do not generate any other content, such as "The caluse is: ...".
    if you have trouble doing it or hold that nothing need to be changed, just return the original sentences,
    the returned sentences is either the Translated sentences or the original sentences, but we encourage you to translate the sentences even if the changes are minor.
    The sentences is: 
    {sentences}
    """

    return_format = '{"sentence1":"","sentence2":"", ...}'

    result, input_tokens, output_tokens = makecomversation(prompt, usercontent, return_format)
    global rough_tranlate_clause_input
    global rough_tranlate_clause_output
    rough_tranlate_clause_input += input_tokens
    rough_tranlate_clause_output += output_tokens
    
    return result, input_tokens, output_tokens


def rough_tranlate(clause_lists):
    clauses = {}
    i = 1
    for clause_list in clause_lists:
        for clause in clause_list:
            clauses[f'clauses{i}'] = clause
            i+=1
  
    result, input_tokens, output_tokens = rough_tranlate_clause(clauses)
    i = 1
    result2 = []
    for clause_list in clause_lists:
        result1 = []
        for clause in clause_list:
            result1.append(result[f'sentence{i}'])
            i+=1
        result2.append(result1)
    return result2, input_tokens, output_tokens

# 精翻译，few shot Translation，作为问题生成的提示  500 tokens
def fewshot_tranlate_clause(clauses, clause_types):
    if len(clause_types) > 2:
        sameple_num = 5
    else:
        sameple_num = 10
    examples = []
    for clause_type in clause_types:
        examples += get_examples(clause_type, sameple_num)

    example_prompt = "Here is some examples:" if len(examples)>0 else ""
    examples = "" if len(examples) == 0 else examples
    prompt = f"""You are a language expert. You need to translate the sql clauses provided and then return the colloquial result. 
    {example_prompt}
    {examples}
    """

    usercontent = f""" You need to translate the sql clauses provided and then return the colloquial result. 
    Do not generate any other content, such as "The paragraph means: ", just the result. 
    if you can't translate the sql clauses, return the clauses provided, don't reply content as such"'The SQL clauses is not valid. Please provide a valid SQL clauses.'".
    The sql clauses is: 
    {clauses}
    """

    return_format = '{"sentence1":"","sentence2":"", ...}'

    result, input_tokens, ouput_tokens = makecomversation(prompt, usercontent, return_format)
    global fewshot_tranlate_clause_input
    global fewshot_tranlate_clause_output
    fewshot_tranlate_clause_input += input_tokens
    fewshot_tranlate_clause_output += ouput_tokens
    return result, input_tokens, ouput_tokens

import random
def get_examples(type, num):
    with open('Translation_examples.txt', 'r') as f:
        Translation_examples = f.readlines()
    examples = []
    if type == 'select':
        select_examples = list(set([line for line in Translation_examples if line.startswith('select')] ))
        random_selection = random.sample(select_examples, num)
    elif type == 'where':
        where_examples = list(set([line for line in Translation_examples if line.startswith('where')] ))
        random_selection = random.sample(where_examples, num)
    elif type == 'order':
        order_examples = list(set([line for line in Translation_examples if line.startswith('order')] ))
        random_selection = random.sample(order_examples, num)
    elif type == 'group':
        order_examples = list(set([line for line in Translation_examples if line.startswith('group')] ))
        random_selection = random.sample(order_examples, 5)
    else: 
        return []
    

    for line in random_selection:
        parts = line.split('|')
        examples.append({'before': parts[0].strip(), 'colloquialized': parts[1].strip()})
    return examples


def get_hint(clause_lists):
    clauses = {}
    clause_types = []
    i = 1
    for clause_list in clause_lists:
        for clause in clause_list:
            clauses[f'clauses{i}'] = clause
            clause_type = clause.split()[0].lower()
            clause_types.append(clause_type)
            i+=1
    
    result, input_tokens, output_tokens = fewshot_tranlate_clause(clauses, list(set(clause_types)))
    i = 1
    result2 = []
    for clause_list in clause_lists:
        result1 = []
        for clause in clause_list:
            result1.append(result[f'sentence{i}'])
            i+=1
        result2.append(result1)

    return result2, input_tokens, output_tokens

def the_final_translate(original_sqls, simplified_versions, hints, descriptions, batch = True):
    if batch:
        return the_final_translate_batch(original_sqls, simplified_versions, hints, descriptions)
    else:
        results = []
        for original_sql, simplified_version, hint in zip(original_sqls, simplified_versions, hints):
            question =  final_translate_one(original_sql, simplified_version, hint, descriptions)
            results.append(question)
        return results  

# 最终翻译  1000~1500 tokens
def the_final_translate_batch(original_sqls, simplified_versions, hints, descriptions):
    with open('spider_examples.txt', 'r', encoding='utf-8') as f:
        spider_examples = f.readlines()
    random_selection = random.sample(spider_examples, 10)

    is_descriptions = descriptions is not None and len(descriptions) > 0
    
    prompt = f"""You are a sqls to question translation expert. You need to translate the sqls provided and then return the coresponding questions easy to understand. 
    Especially, when "count(stuff_id)" or "group by stuff_id", we means "how many stuff are there", or "for each stuff", not how many ids are there, don't mention id or IDS if not necessary. 
    and don't use the word "count" or orther function name in the question, say what they do.
    Also, don't mention the table name or column name in the question, or use the word "table" or "column" in the question, guess the realistic meaning from the table name, 
    such as table "address.address" is just a address, the "address.last_update" is just the last update time.
    don't use from clause in the question, and don't use the word "from" in the question, people who ask the question don't need to know where the data is stored.
    
    here is some examples:
    {random_selection}
    """

    usercontent = f""" You need to translate the sqls provided and then return coresponding questions. 
    Because sometimes sql is too complex to understand, or even contains errors, we will also provide a simplified version(a clause list, contains main information about the sql) for reference. 
    In addition, we will also provide some tips to introduce the meaning of this sqls, and what the generated question is mostly about.
    Do not generate any other content, such as "The question is: ", just the question of the sqls itself. 
    if you can't translate the sqls, return the simplified version provided(needs to be concat in right order), don't reply content as such "The sqls clause is not valid. Please provide a valid SQL clause.".
    """ 

    if is_descriptions:
        temp = f"""
        We will provide the descriptions of the columns in sqls, which you can take as reference.
        """
        usercontent += temp
    
    inputs = {}
    i = 1
    for original_sql, simplified_version, hint in zip(original_sqls, simplified_versions, hints):
        inputs[f'batch{i}'] = {}
        inputs[f'batch{i}']['original_sql'] = original_sql
        inputs[f'batch{i}']['simplified_sql'] = simplified_version
        inputs[f'batch{i}']['question_hint'] = hint
        i += 1
    usercontent += f"""
    The sqls are: 
    {inputs}
    """

    if is_descriptions:
        usercontent += f"""
        The descriptions of the columns are:
        {descriptions}
        """

    return_format = '{"question1":"","question2":"", ...}'

    result, input_tokens, ouput_tokens = makecomversation(prompt, usercontent, return_format)
    global the_final_translate_input
    global the_final_translate_output
    the_final_translate_input += input_tokens
    the_final_translate_output += ouput_tokens
    result1 = []
    i =1
    for item in result:
        result1.append(result[f'question{i}'])
        i+=1
    return result1, input_tokens, ouput_tokens

def final_translate_one(original_sql, simplified_version, hints, descriptions):
    with open('spider_examples.txt', 'r', encoding='utf-8') as f:
        spider_examples = f.readlines()
    random_selection = random.sample(spider_examples, 10)

    is_descriptions = descriptions is not None and len(descriptions) > 0
    
    prompt = f"""You are a sql to question translation expert. You need to translate the sql provided and then return the coresponding question easy to understand. 
    Especially, when "count(stuff_id)" or "group by stuff_id", we means "how many stuff are there", or "for each stuff", not how many ids are there, don't mention id or IDS if not necessary. 
    and don't use the word "count" or orther function name in the question, say what they do.
    Also, don't mention the table name or column name in the question, or use the word "table" or "column" in the question, guess the realistic meaning from the table name, 
    such as table "address.address" is just a address, the "address.last_update" is just the last update time.
    don't use from clause in the question, and don't use the word "from" in the question, people who ask the question don't need to know where the data is stored.
    most sql i provided contains meaningless parts, if possible, try to ignore those meaningless part in the question.
    here is some examples:
    {random_selection}
    """

    usercontent = f""" You need to translate the sql provided and then return coresponding question. 
    Because sometimes SQL is too complex to understand, or even contains errors, we will also provide a simplified version(a clause list, contains main information about the sql) for reference. 
    In addition, we will also provide some tips to introduce the meaning of this sql, and what the generated question is mostly about.
    Do not generate any other content, such as "The question is: ", just the question of the sql itself. 
    if you can't translate the sql, return the simplified version provided(needs to be concat in right order), don't reply content as such "The SQL clause is not valid. Please provide a valid SQL clause.".
    """ 
    if is_descriptions:
        temp = f"""
        We will provide the descriptions of the columns in SQL, which you can take as reference.
        """
        usercontent += temp
    

    usercontent +=f"""
    The original sql is: 
    {original_sql}
    The simplified version is:
    {simplified_version}
    The hints are:
    {hints}
    """
    if is_descriptions:
        usercontent += f"""
        The descriptions of the columns are:
        {descriptions}
        """

    return_format = '{"question":" coresponding question to the sql provided"}'

    result, input_tokens, ouput_tokens = makecomversation(prompt, usercontent, return_format)
    global the_final_translate_input
    global the_final_translate_output
    the_final_translate_input += input_tokens
    the_final_translate_output += ouput_tokens
    return result['question'], input_tokens, ouput_tokens

def getfileinfo_from_path(path):
    # 获取文件名
    file_name = os.path.basename(path)

    # 获取文件类型
    file_name, file_type = file_name.split('.')
    return file_name, file_type

# random fewshot 翻译 300tokens
def en2ch(ens):
    inputs = {}
    i = 1
    for en in ens:
        inputs[f'english{i}'] = en
        i+=1

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
    "for each unique aircraft code" 可以翻译为"不同飞机代码" 而不是"每个独特的飞机代码"。
    here are some examples:
    {examples}
    """

    usercontent = f""" Translate the chinese questions provided below, then return the translated english questions.
    The english questions is: {inputs} 
    """

    return_format = '{"chinese1":"","chinese2":"", ...}'

    result, input_tokens, output_tokens = makecomversation(prompt, usercontent, return_format)
    global en2ch_input
    global en2ch_output
    en2ch_input += input_tokens
    en2ch_output += output_tokens
    result1 = []
    for i, item in enumerate(result):
        result1.append(result[f'chinese{i+1}'])
    return result1, input_tokens, output_tokens

# 集合上面方法
def sql2question(sqls, db_name = None, jump= True, batch = True):
    
    # 预处理
 
    preprocessed_sqls, inputs1, inputs2, outputs1, outputs2 = preprocess(sqls, jump)

    clause_lists = []
    for sql in preprocessed_sqls:
        clause_list = get_clause(sql)
        clause_lists.append(clause_list)
    afterprocessed_clauses = []
    decomposed_clause_list = [] # for get descriptions
    for clause_list in clause_lists:
        decomposed_clause = after_process(clause_list)
        decomposed_clause_list += decomposed_clause
        afterprocessed_clauses.append(decomposed_clause)

    # 知识生成
    try: 
        descriptions = get_sql_descriptions(decomposed_clause_list, db_name)
    except Exception as e:
        print("can't get descriptions:", e)
        descriptions = 'no descriptions available, you have to guess from the table name.'


    simplified_sql, inputs3, outputs3 = rough_tranlate(afterprocessed_clauses)
    hints, inputs4, outputs4 = get_hint(simplified_sql)
    
    # 翻译
    questions, inputs5, outputs5 = the_final_translate(sqls, simplified_sql, hints, descriptions, batch)
    
    # 将token统计数目保存到本地文件
    with open('token_count.txt', 'a') as f:
        f.write(f"remove_aliases: {remove_aliases_input} {remove_aliases_output}\n")
        f.write(f"place_tablename: {place_tablename_input} {place_tablename_output}\n")
        f.write(f"rough_tranlate_clause: {rough_tranlate_clause_input} {rough_tranlate_clause_output}\n")
        f.write(f"fewshot_tranlate_clause: {fewshot_tranlate_clause_input} {fewshot_tranlate_clause_output}\n")
        f.write(f"the_final_translate: {the_final_translate_input} {the_final_translate_output}\n")
    # print("remove_aliases:",remove_aliases_input, remove_aliases_output)
    # print("place_tablename:",place_tablename_input, place_tablename_output)
    # print("rough_tranlate_clause:",rough_tranlate_clause_input, rough_tranlate_clause_output)
    # print("fewshot_tranlate_clause:",fewshot_tranlate_clause_input, fewshot_tranlate_clause_output)
    # print("the_final_translate:",the_final_translate_input, the_final_translate_output)

    inputs = [inputs1, inputs2, inputs3, inputs4, inputs5]
    outputs = [outputs1, outputs2, outputs3, outputs4, outputs5]
    return questions, inputs, outputs
    

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description='SQL to question translation')

    # random seed
    parser.add_argument('--sql_path', type=str, default='salika_sqls.txt', help='输入文件')
    parser.add_argument('--output_path', type=str, default='new_salika.txt', help='结果输出文件')
    parser.add_argument('--json_sql_indicator', type=str, default='sql', help='json文件的保存sql语句的key')
    parser.add_argument('--jump', type=bool, default=True, help='是否跳过预处理')
    parser.add_argument('--batchsize', type=int, default=10, help='每次提交的sql数量')
    parser.add_argument('--final_batch', type=bool, default=True, help='是否在最终翻译时使用batch模式')
    args = parser.parse_args()

    sql_path = args.sql_path
    output_path = args.output_path
    sql_indicator = args.json_sql_indicator
    batchsize = args.batchsize
    jump_preprocess = args.jump
    final_batch = args.final_batch
    print(sql_path, output_path)
    start_time = time.time()

    
    filename, filetype = getfileinfo_from_path(sql_path)

    # 读文件
    with open(sql_path, 'r',encoding='utf-8') as file:
        if filetype == 'json':
            jsonfile = json.load(file)
            original_sqls = []
            for item in jsonfile:
                original_sqls.append(item[sql_indicator])
        else:
            original_sqls = file.readlines()
    

    total_number  = len(original_sqls)
    
    print("read sqls successfully!, total number of sqls: ", total_number, "\n\n")


    bar = Bar(f'{sql_path}:', max=math.ceil(total_number / batchsize))
    sql_question_pairs = []
    err_list = []
    sql2en_token_count = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # key: future object, value: input sql
        future_to_sentence = {executor.submit(lambda paramters: sql2question(*paramters), [original_sqls[i:i+batchsize], filename, jump_preprocess, final_batch]): original_sqls[i:i+batchsize] for i in range(0, len(original_sqls), batchsize)}
        
        for future in concurrent.futures.as_completed(future_to_sentence):
            original_sqls = future_to_sentence[future]
            
            bar.next()
            try:
                questions, input_token_list, output_token_list = future.result()
                if len(questions) != len(original_sqls):
                    print("Error: the number of questions is not equal to the number of sqls")
                    for original_sql in original_sqls:
                        err_list.append(original_sql)
                    continue
                for original_sql, question in zip(original_sqls, questions):
                    # 无法保证gpt按正确顺序输出
                    sql_question_pairs.append({'sql': original_sql, 'question': question})
                    # sql2en_token_count.append({'sql':original_sql,"input":input_token_list,"output":output_token_list})
                sql2en_token_count.append({'sqls':original_sqls,"input":input_token_list,"output":output_token_list,"total_input": sum(input_token_list),"total_output":sum(output_token_list)})
            except Exception as e:
                print("While translate sql sentences:",original_sqls,", an errir occurred:", e)
                for original_sql in original_sqls:
                    err_list.append(original_sql)
    
    end_time = time.time()  
    total_time = end_time - start_time
    print(f"\n\ngenerate question for {sql_path} over, {len(err_list)} filed, total time cost {total_time} seconds\n\n")

    english_question = [pair['question'] for pair in sql_question_pairs]
    total_number  = len(english_question)
    bar = Bar(f'{sql_path}:', max=math.ceil(total_number / batchsize))
    err_list = []
    en_ch_pairs = []

    start_time = time.time()
    en2ch_token_count = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_sentence = {executor.submit(en2ch, english_question[i:i+batchsize]): english_question[i:i+batchsize] for i in range(0, len(english_question), batchsize)}
        for future in concurrent.futures.as_completed(future_to_sentence):
            ens = future_to_sentence[future]
            bar.next()
            try:
                chs, inputs, outputs = future.result()
                if len(chs) != len(ens):
                    print("Error: the number of chinese questions is not equal to the number of english questions")
                    for en in ens:
                        err_list.append(en)
                    continue
                for en, ch in zip(ens, chs):
                    en_ch_pairs.append({'en': en, 'ch': ch})
                    # en2ch_token_count.append({'en':en,"input":inputs,"output":outputs})
                en2ch_token_count.append({'ens':ens,"input":inputs,"output":outputs})
            except Exception as e:
                print("翻译句子",en,"时出现异常:", e)
                err_list.append(en)

    end_time = time.time()  
    total_time = end_time - start_time
    print(f"translate question for {sql_path} finishied. {len(err_list)} total time cost {total_time} seconds\n\n")

    with open('total_token_count.txt', 'a+',encoding='utf-8') as f:
        total_input_token = sum([item['total_input'] for item in sql2en_token_count])+sum([item['input'] for item in en2ch_token_count])
        total_output_token = sum([item['total_output'] for item in sql2en_token_count])+sum([item['output'] for item in en2ch_token_count])
        f.write(f"{sql_path}, {output_path}, tokens_consumed, prompt: {total_input_token}, output: {total_output_token}\n\n")

    with open('detail_token_count.json', 'a+',encoding='utf-8') as f:
        f.write(json.dumps({"sql2en":sql2en_token_count, "en2ch":en2ch_token_count}, indent=4, ensure_ascii=False))
        f.write('\n\n')

    # merge
    for item in sql_question_pairs:
        for en_ch_pair in en_ch_pairs:
            if item['question'] == en_ch_pair['en']:
                item['ch'] = en_ch_pair['ch']
                break
    
    output_dir = os.path.dirname(output_path)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    # 写文件
    with open(output_path, 'w', encoding="utf-8") as file:
        if filetype == 'json':
            jsonresults = []
            # 找到json item的sql和sql_question_pairs的sql对应
            for item in jsonfile: # 为每一个json item找到对应的问题，并添加问题
                for pair in sql_question_pairs:
                    if pair['sql'] == item[sql_indicator]:
                        item['question'] = pair['question']
                        item['chinese question'] = pair['ch']
                        jsonresults.append(item)
                        break # 跳出
            json.dump(jsonresults, file, indent=4, ensure_ascii=False)
        else:
            for item in sql_question_pairs:
                file.write(f"{item['sql']}\n{item['question']}\n{item['ch']}\n\n")
    print(f"file write to {output_path}\n\n")