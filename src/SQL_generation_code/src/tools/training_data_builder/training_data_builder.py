import argparse
import copy
import json
from pathlib import Path
from typing import List

from spacy.lang.en import English

from manual_inference.helper import get_schemas_cordis, tokenize_question, get_schema_hack_zurich, get_schema_sdss, get_schemas_spider, get_schema_oncomx, get_schemas_worldcup
from spider.test_suite_eval.process_sql import get_sql
from tools.training_data_builder.schema import build_schema_mapping, SchemaIndex
import logging

logger = logging.getLogger(__name__)
FORMAT = "[%(filename)s:%(lineno)s - %(funcName)20s() ]\n%(message)s"
logging.basicConfig(format=FORMAT)

def transform_sample(sample, schema_dict, tokenizer):
    database = sample['db_id']
    query = sample['query']
    question = sample['question']

    schema_mapping = build_schema_mapping(schema_dict[database])
    schema = SchemaIndex(
        schema_mapping, schema_dict[database]['column_names_original'], schema_dict[database]['table_names_original'])

    spider_sql_structure, sql_tokenized = get_sql(schema, query)

    return {
        'db_id': database,
        'question': question,
        'question_toks': tokenize_question(tokenizer, question),
        'query': query,
        'sql': spider_sql_structure,
        'query_toks': sql_tokenized,
    }


def main(args: argparse.Namespace):
    nlp = English()

    # load schema necessary for your training data.
    if args.data == 'cordis':
        _, schemas_dict, _, _ = get_schemas_cordis()
    elif args.data == 'hack_zurich':
        _, schemas_dict, _ = get_schema_hack_zurich()
    elif args.data == 'skyserver_dr16_2020_11_30':
        _, schemas_dict, _ = get_schema_sdss()
    elif args.data == 'oncomx':
        _, schemas_dict, _ = get_schema_oncomx()
    elif args.data == 'spider':
        _, schemas_dict, _, _ = get_schemas_spider()
    elif args.data == 'world_cup_data_v2':
        _, schemas_dict, _, _ = get_schemas_worldcup()
    else:
        raise ValueError('Dataset not yet supported')

    # There can be multiple files with training data which we will concatenate.
    # the training data needs to be an array of object each having the following properties:
    # 'db_id' --> name of the database
    # 'question' --> natural language question
    # 'query' --> SQL query as one string

    seed_sample_paths: List[Path] = []

    # this is usually where the human-made training data exists
    human_made_seed_data_path = Path(f'data/{args.data}/handmade_training_data/generative_data_train.json')
    # human_made_seed_data_path = Path(f'data/{args.data}/generative/all_synthetic.json')
    if human_made_seed_data_path.exists():
        seed_sample_paths.append(human_made_seed_data_path)

    # this is usually where the synthetic, GPT-3 based training data exists
    # synthetic_data_path = Path(f'data/{args.data}/generative/all_synthetic.json')
    # if synthetic_data_path.exists():
    #    training_sample_paths.append(synthetic_data_path)

    # we should not use that data anymore

    # if args.data == 'cordis':
    #     training_sample_paths.append(Path('data/cordis/trees/all_adapted.json'))

    samples = []
    n_not_successful = 0
    for path in seed_sample_paths:
        with open(path, 'r', encoding='utf-8') as file_handle:
            data = json.load(file_handle)

            for sample in data:
                try:
                    transformed = transform_sample(sample, schemas_dict, nlp.tokenizer)
                    samples.append(transformed)
                except Exception as e:
                    print(f'Error while transforming sample: {e}')
                    print(f'Sample: {sample}')
                    n_not_successful += 1


    print(f'successfully transformed {len(samples)} samples for seed split. {n_not_successful} samples could not be transformed.')

    with open(Path(f'data/{args.data}/original/generative_data_train.json'), 'w', encoding='utf-8') as f:
    # with open(Path(f'data/{args.data}/original/all_synthetic.json'), 'w', encoding='utf-8') as f:
        json.dump(samples, f, indent=2)

    dev_sample_paths: List[Path] = []

    # this is usually where the human-made training data exists
    human_made_dev_data_path = Path(f'data/{args.data}/handmade_training_data/handmade_data_dev.json')
    if human_made_dev_data_path.exists():
        dev_sample_paths.append(human_made_dev_data_path)
    
    samples = []
    n_not_successful = 0
    for path in dev_sample_paths:
        with open(path, 'r', encoding='utf-8') as file_handle:
            data = json.load(file_handle)

            for sample in data:
                try:
                    transformed = transform_sample(sample, schemas_dict, nlp.tokenizer)
                    samples.append(transformed)
                except Exception as e:
                    print(f'Error while transforming sample: {e}')
                    print(f'Sample: {sample}')
                    n_not_successful += 1

    print(f'successfully transformed {len(samples)} samples for dev split. {n_not_successful} samples could not be transformed.')

    with open(Path(f'data/{args.data}/original/dev.json'), 'w', encoding='utf-8') as f:
        json.dump(samples, f, indent=2)



if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument(
        '--data', type=str, choices=['cordis', 'hack_zurich', 'skyserver_dr16_2020_11_30', 'spider', 'oncomx' ,'world_cup_data_v2'], required=True)

    args = arg_parser.parse_args()
    main(args)
