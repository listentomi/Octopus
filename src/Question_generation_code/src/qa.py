import json
import yaml
import os
from openai import APIConnectionError, OpenAI

def load_config(file_path):
    with open(file_path, 'r') as config_file:
        config = yaml.safe_load(config_file)
    return config

config = load_config('config.yaml')

# os.environ["https_proxy"] = "http://localhost:10809"

client = OpenAI(
    api_key=config['api']['key']
)



def makecomversation(prompt, usercontent, return_format, temperature=0):
    def sendquestion(prompt, usercontent):
        message = [
                {
                    "role": "system",
                    "content": prompt 
                },
                {
                    "role": "user",  
                    "content": usercontent + ". Make sure to return the result in JSON format: " + return_format
                }
            ]
        
        chat_completion = client.chat.completions.create(
            # model="gpt-3.5-turbo-1106",
            model="gpt-4-turbo", # gpt-4-turbo-preview
            messages=message,
            temperature=temperature,
            response_format={"type": "json_object"}
            )
        return chat_completion

    try:
       chat_completion = sendquestion(prompt, usercontent)
    except Exception as e: 
       chat_completion = sendquestion(prompt, usercontent)
       
    answer = chat_completion.choices[0].message.content
    completion_tokens = chat_completion.usage.completion_tokens 
    prompt_tokens = chat_completion.usage.prompt_tokens
    print(answer)

    return json.loads(answer), prompt_tokens, completion_tokens

if __name__=="__main__":
    print(makecomversation(prompt='hello',usercontent='test',return_format=''))