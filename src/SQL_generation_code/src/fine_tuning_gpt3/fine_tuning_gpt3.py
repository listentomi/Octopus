import openai
import logging
import json
import os
import time
from pytictoc import TicToc
from pathlib import Path
from dotenv import load_dotenv
logger = logging.getLogger(__name__)
FORMAT = "[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
logging.basicConfig(format=FORMAT, level=logging.INFO)
load_dotenv() # retrieve OPENAI_API_KEY
openai.api_key = os.getenv("OPENAI_API_KEY")


def prepare_fine_tune_data(input_json_file, output_jsonl_file):
    """
    Training data must be in JSONL document
    
    Example:

    {"prompt": "<prompt text>", "completion": "<ideal generated text>"}
    {"prompt": "<prompt text>", "completion": "<ideal generated text>"}
    {"prompt": "<prompt text>", "completion": "<ideal generated text>"}
    ...

    """
    try:
        with open(input_json_file, 'r') as f_in:
            data = json.load(f_in)
        lines = []
        for d in data:
            s = {'prompt': d['query'], 'completion': d['question']}
            json_str = json.dumps(s)
            lines.append(json_str)
        Path(output_jsonl_file).parent.mkdir(parents=True, exist_ok=True)
        if not Path(output_jsonl_file).exists():
            with open(output_jsonl_file, 'w') as f_out:        
                for line in lines:
                    f_out.writelines(line + '\n')
            logging.warning(f"file {output_jsonl_file} generated successfully!")
        else:
            logging.warning(f"file {output_jsonl_file} already existed. No file was generated!")
    except FileExistsError as e:
        logging.error(str(e.__traceback__))

def upload_training_data(jsonl_file, delay=3):
    """returned example
    {
     "bytes": 495,
    "created_at": 1654005243,
    "filename": "gpt_ft_test.jsonl",
    "id": "file-y9MHYvfS8QP4cI7rYWNKbr6G",
    "object": "file",
    "purpose": "fine-tune",
    "status": "uploaded",
    "status_details": null
    }
    """
    with open(jsonl_file, 'r') as f_in:
        try:
            response = openai.File.create(file=open(jsonl_file), purpose="fine-tune")
            file_id = response['id']
            t = TicToc()
            t.tic()
            while response['status'] != 'processed':
                time.sleep(3)
                response = openai.File.retrieve(file_id)
        except Exception as e:
            logging.error(str(e.__traceback__))

def check_upload_file(file_id):
    res = False
    try:
        response = openai.File.retrieve(id=file_id)
        if response['status'] == 'processed':
            res = True
    except Exception as e:
        logging.error(str(e.__traceback__))
    return res

def fine_tune(file_id, name=None, user=None, delay=3, model='text-davinci-002'):
    if check_upload_file(file_id):
        t = TicToc()
        t.tic()
        response = openai.FineTune.create(training_file=file_id)
        ft_id = response['id']
        logging.info(response)
        while response['status'] != 'succeeded':
            time.sleep(delay)
            response = openai.FineTune.retrieve(id=ft_id)
            logger.info(response)
        t.toc()
    
    # # 微调任务完成后，获取快照列表
    #     snapshots = openai.FineTune.list_snapshots(ft_id)
    #     if snapshots and 'snapshots' in snapshots:
    #         snapshot_id = snapshots['snapshots'][0]['id']  # 选择第一个快照
    #         # 下载模型快照
    #         snapshot_data = openai.FineTune.download_snapshot(snapshot_id)
    #         with open('fine_tuned_model.tar.gz', 'wb') as f:
    #             f.write(snapshot_data)

    #     logger.info("Fine-tuned model saved.")

def main():
    input_json_file = 'C:/Users/86130/Downloads/sql/data/power/handmade_training_data/gpt_ft_test.json'
    output_jsonl_file = 'C:/Users/86130/Downloads/sql/data/power/fine_tune/gpt_ft_test.jsonl'
    # Step 1. Prepare the jsonl file
    #prepare_fine_tune_data(input_json_file, output_jsonl_file)
    # Step 2. Upload the jsonl file
    upload_training_data(output_jsonl_file)
    # Step 3.
    # Check the status of the uploaded file
    #check_upload_file("file-zBBCFyA4wYbjw28iWe0diAyX")
    # Step 4.
    #Finetune the gpt-3 model
    #fine_tune("file-zBBCFyA4wYbjw28iWe0diAyX")

if __name__ == '__main__':
    main()
