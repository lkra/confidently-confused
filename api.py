import json
import time

import requests
import openai

from dotenv import dotenv_values
from utils import gpt3, chatgpt

CONFIG = dotenv_values(".env")
AVAILABLE_APIS = [
     'huggingface',
     'gpt3',
     'chatgpt',
]

def query(payload, headers, url):
        data = json.dumps(payload)
        response = requests.request("POST", url, headers=headers, data=data)
        if response.status_code != 200:
            print(payload)
            print(response)
        response_data = json.loads(response.content.decode("utf-8"))
        return response_data

def call_api_hf(prompt, model="gpt2"):
    url = f"https://api-inference.huggingface.co/models/{model}"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {CONFIG['HF_API_TOKEN']}"
    }
    data = query({'inputs': prompt, 'options':{'wait_for_model': True}}, headers, url)
    return data

def get_response(prompt, api="huggingface", model="gpt2"):
    if api == "huggingface":
        response = call_api_hf(prompt, model=model)
    elif api == 'gpt3':
        openai.api_key = CONFIG['OPENAI_API_TOKEN']
        response = gpt3([prompt], model=model)
    elif api == 'chatgpt':
        openai.api_key = CONFIG['OPENAI_API_TOKEN']
        response = chatgpt([prompt], model=model)
    else:
        raise ValueError(f"API {api} not available. Available APIs: {AVAILABLE_APIS}")

    return response



if __name__ == "__main__":
    CERTAINTY_PREPEND = "For every message here onwards, prepend a score denoting your certainty on a range between 0 being very uncertain, and 1 being very certain. An example looks like this: Question: What is the capital of France? Answer: [1.0] Paris. Question: "

    with open("questions.txt", "r") as f:
        for line in f:
            print(line)
            response = get_response(CERTAINTY_PREPEND + line, model='OpenAssistant/oasst-sft-4-pythia-12b-epoch-3.5')
            # remove line from response
            response = response[0]['generated_text'].replace(CERTAINTY_PREPEND + line, "")
            print(response)
            print("+===========+")

