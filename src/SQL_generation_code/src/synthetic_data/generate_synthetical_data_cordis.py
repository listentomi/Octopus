import argparse
import csv
import json
import os
import re
import time
from pathlib import Path
from types import SimpleNamespace
import sys
import os

# 将当前工作目录添加到 Python 模块搜索路径
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)
# 获取父目录路径
parent_dir = os.path.dirname(current_dir)
# 将父目录路径添加到 Python 模块搜索路径
sys.path.append(parent_dir)
import openai
from typing import List

from common_query_types import common_query_types
from group_pairs_to_find_templates import group_query_types, map_semql_actions_only
from sample_queries.sample_query import sample_query
from tools.transform_generative_schema import GenerativeSchema
from dotenv import load_dotenv

load_dotenv()

"""
Synthetic data generator by using Ursin's templates
"""

def ask_gpt(sample: str, number_of_choices: int, model_id: str, sec=3):
    # there is no need to to query engineering - we use a fine-tuned GPT3 model instead.
    response = None
    #prompt = sample + '\n\n###\n\n'
    #prompt = "Generate a question that can guide the user to generate a query similar to the given SQL statement:\n\n" + sample + "\n\n###\n\n"
    prompt = "Generate a question related to the following SQL statement:\n\n" + sample + "\n\nExample question:"
    while response is None:
        try:
            response = openai.Completion.create(
                model="text-davinci-002",
                prompt=prompt,
                # top_p=0.9,
                max_tokens=128,
                n=number_of_choices,
                # frequency_penalty=0.5,
                # presence_penalty=0.5,
                #stop=["\n"]
                stop=None
            )
            time.sleep(sec)
            print(f"sleep {sec} sec...")
        except Exception as e:
            print(f"{e}")
            sec += sec
            time.sleep(sec)
            pass
    print(response)
    # for choice in response.choices:
    #     print(choice.text)
    return response, prompt


def main(args):

    #with open(Path(args.data_path) / 'original' / 'tables.json') as f:
    with open('C:/Users/86130/Downloads/sql/data/power/table.json', encoding='utf-8') as f:
        schemas = json.load(f)
        original_schema = schemas[0]  # we assume there is only one db-schema in this file

    #generative_schema = GenerativeSchema(Path(args.data_path) / 'generative' / 'generative_schema.json')
    generative_schema = GenerativeSchema(Path('C:/Users/86130/Downloads/sql/data/power/generative/generative_schema.json'))

    db_config = SimpleNamespace(database=args.database,
                                db_user=args.db_user,
                                db_password=args.db_password,
                                db_host=args.db_host,
                                db_port=args.db_port,
                                db_options=args.db_options,
                                path = args.db_path)

    query_cache = []

    for idx, (query_type, multiplier) in enumerate(common_query_types().items()):

        round_idx = 0
        fail_to_sample = 0

        # we might have to repeat the sampling process multiple times to get enough samples (exceptions due to unfavorable samplings),
        # but we still don't want to be caught in an infinite loop.
        while round_idx < (args.base_number_of_samples_per_query_type * multiplier) and fail_to_sample < 50:

            try:
                sampled_query, sampled_query_replaced = sample_query(query_type, original_schema, generative_schema, db_config)

                if sampled_query in query_cache:
                    raise ValueError('Query already sampled')
                else:
                    query_cache.append(sampled_query)

                print(f'{query_type}                        {sampled_query}')
                print(sampled_query_replaced)
                response, prompt = ask_gpt(sampled_query_replaced, args.number_of_choices, args.gpt3_finetuned_model)

                gpt_choices = [f"({idx}) {c['text'].strip()}" for idx, c in enumerate(response['choices'])]

                with open(Path(args.output_folder) / f'{idx}_{round_idx}.txt', 'w') as f:
                    f.write(prompt)
                    f.write('\nOriginal Query:\n')
                    f.write(sampled_query)
                    f.write('\nGPT-3 choices:\n')
                    f.write('\n'.join(gpt_choices))

                round_idx += 1

            except ValueError as e:
                print(f'Exception:{e}')
                fail_to_sample += 1

        print()
        print()


if __name__ == '__main__':
    openai.api_key = os.getenv("OPENAI_API_KEY")
    openai.api_key = 'sk-KIuv9VzNDqsC4otPqo4m9IUqCUnnVAvn7SuNQqLMouA5TGy0'

    arg_parser = argparse.ArgumentParser()
    #arg_parser.add_argument('--data_path', type=str, default='data/cordis')
    arg_parser.add_argument('--output_folder', type=str, default='C:/Users/86130/Downloads/sql/data/power')
    arg_parser.add_argument('--number_of_choices', type=int, default=4)
    arg_parser.add_argument('--base_number_of_samples_per_query_type', type=int, default=30, help='The base number of samples per query type. '
                                                                                                 'This number, multiplied with the query type multiplier (see "common_query_types.py") '
                                                                                                 'is the total number of samples that will be generated for each query type.')

    arg_parser.add_argument('--database', type=str, default='cordis_temporary')
    arg_parser.add_argument('--db_path', type=str, default='C:/Users/86130/Downloads/sql/data/power/test.db')
    arg_parser.add_argument('--db_user', type=str, default='postgres')
    arg_parser.add_argument('--db_password', type=str, default='vdS83DJSQz2xQ')
    arg_parser.add_argument('--db_host', type=str, default='testbed.inode.igd.fraunhofer.de')
    arg_parser.add_argument('--db_port', type=str, default='18001')
    arg_parser.add_argument('--db_options', type=str, default=f"-c search_path=unics_cordis,public")
    arg_parser.add_argument('--gpt3_finetuned_model', type=str, default='davinci:ft-personal-2022-01-17-10-28-10')
    args = arg_parser.parse_args()
    main(args)