import json
import random
import time
from tqdm import tqdm
import multiprocessing
from concurrent.futures import ThreadPoolExecutor
import openai
import os
import argparse
from prompts import *


class ChatGPTProcessor:
    def __init__(self):
        self.lock = multiprocessing.Lock()
        openai.api_key = ""
        openai.api_base = ""

    def read_jsonl(self, input_file):
        with open(input_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        return list(map(json.loads, tqdm(lines, desc='Reading...')))

    def write_to_json(self, data, file_path):
        with self.lock:
            with open(file_path, 'a', encoding='utf-8') as file:
                json.dump(data, file, ensure_ascii=False)
                file.write('\n')

    def multiple_gpt(self, payload):
        while True:
            try:
                chat_completion = openai.ChatCompletion.create(model=payload['model'], temperature=0, messages=payload['messages'])
                data = payload.copy()
                data['messages'] = payload['messages']
                data['answer'] = payload['answer']
                data['output'] = chat_completion.choices[0].message.content
                break
            except Exception as e:
                time.sleep(random.randint(1, 3))

        self.write_to_json(data, payload['save_path'])
        time.sleep(random.randint(1, 3))



def format_prompt_4(d, args):
    if args.language == 'zh':
        cA = d['选项A'].replace("A. ", "")
        cB = d['选项B'].replace("B. ", "")
        cC = d['选项C'].replace("C. ", "")
        cD = d['选项D'].replace("D. ", "")
        choices = [cA, cB, cC, cD]
        random.shuffle(choices)
        prompt = UserEvaluatePrompt4Choices_zh.format(story=d['故事'], question=d['问题'], choice_a=choices[0], choice_b=choices[1], choice_c=choices[2], choice_d=choices[3])
        map = {"A": "", "B": "", "C": "", "D": ""}

        if choices[0] == cA:
            map['A'] = 'A'
        elif choices[0] == cB:
            map['A'] = 'B'
        elif choices[0] == cC:
            map['A'] = 'C'
        elif choices[0] == cD:
            map['A'] = 'D'
        
        if choices[1] == cA:
            map['B'] = 'A'
        elif choices[1] == cB:
            map['B'] = 'B'
        elif choices[1] == cC:
            map['B'] = 'C'
        elif choices[1] == cD:
            map['B'] = 'D'

        if choices[2] == cA:
            map['C'] = 'A'
        elif choices[2] == cB:
            map['C'] = 'B'
        elif choices[2] == cC:
            map['C'] = 'C'
        elif choices[2] == cD:
            map['C'] = 'D'
        
        if choices[3] == cA:
            map['D'] = 'A'
        elif choices[3] == cB:
            map['D'] = 'B'
        elif choices[3] == cC:
            map['D'] = 'C'
        elif choices[3] == cD:
            map['D'] = 'D'
    else:
        cA = d['OPTION-A'].replace("A. ", "")
        cB = d['OPTION-B'].replace("B. ", "")
        cC = d['OPTION-C'].replace("C. ", "")
        cD = d['OPTION-D'].replace("D. ", "")
        choices = [cA, cB, cC, cD]
        random.shuffle(choices)
        prompt = UserEvaluatePrompt4Choices_en.format(story=d['STORY'], question=d['QUESTION'], choice_a=choices[0], choice_b=choices[1], choice_c=choices[2], choice_d=choices[3])
        map = {"A": "", "B": "", "C": "", "D": ""}

        if choices[0] == cA:
            map['A'] = 'A'
        elif choices[0] == cB:
            map['A'] = 'B'
        elif choices[0] == cC:
            map['A'] = 'C'
        elif choices[0] == cD:
            map['A'] = 'D'
        
        if choices[1] == cA:
            map['B'] = 'A'
        elif choices[1] == cB:
            map['B'] = 'B'
        elif choices[1] == cC:
            map['B'] = 'C'
        elif choices[1] == cD:
            map['B'] = 'D'

        if choices[2] == cA:
            map['C'] = 'A'
        elif choices[2] == cB:
            map['C'] = 'B'
        elif choices[2] == cC:
            map['C'] = 'C'
        elif choices[2] == cD:
            map['C'] = 'D'
        
        if choices[3] == cA:
            map['D'] = 'A'
        elif choices[3] == cB:
            map['D'] = 'B'
        elif choices[3] == cC:
            map['D'] = 'C'
        elif choices[3] == cD:
            map['D'] = 'D'
    return map, prompt


def format_prompt_2(d, args):
    if args.language == 'zh':
        cA = d['选项A'].replace("A. ", "")
        cB = d['选项B'].replace("B. ", "")
        choices = [cA, cB]
        random.shuffle(choices)
        prompt = UserEvaluatePrompt2Choices_zh.format(story=d['故事'], question=d['问题'], choice_a=choices[0], choice_b=choices[1])
        map = {"A": "", "B": "", "C": "", "D": ""}
        if choices[0] == cA:
            map['A'] = 'A'
        elif choices[0] == cB:
            map['A'] = 'B'
        
        if choices[1] == cA:
            map['B'] = 'A'
        elif choices[1] == cB:
            map['B'] = 'B'
    else:
        cA = d['OPTION-A'].replace("A. ", "")
        cB = d['OPTION-B'].replace("B. ", "")
        choices = [cA, cB]
        random.shuffle(choices)
        prompt = UserEvaluatePrompt2Choices_en.format(story=d['STORY'], question=d['QUESTION'], choice_a=choices[0], choice_b=choices[1])
        map = {"A": "", "B": "", "C": "", "D": ""}
        if choices[0] == cA:
            map['A'] = 'A'
        elif choices[0] == cB:
            map['A'] = 'B'
        
        if choices[1] == cA:
            map['B'] = 'A'
        elif choices[1] == cB:
            map['B'] = 'B'

    return map, prompt


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--task", type=str, default="")
    parser.add_argument("--model_name", type=str, default="")
    parser.add_argument("--api_base", type=str, default="")
    parser.add_argument("--api_key", type=str, default="")
    parser.add_argument("--language", type=str, default="zh")
    parser.add_argument("--try_times", type=int, default=5)
    parser.add_argument("--cot", type=bool, default=False)
    parser.add_argument('--output_path', type=str, default="./results")
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    random.seed(args.seed)
    processor = ChatGPTProcessor()

    files = os.listdir("./data")
    if args.task != "":
        files = [args.task]

    for file in files:
        task = file.split(".")[0]
        try:
            with open(f"data/{file}", "r", encoding='utf-8') as f:
                data = [json.loads(line) for line in f.readlines()]
        except:
            continue
        payloads = []
        for i, d in enumerate(data):
            for j in range(args.try_times):
                if d['选项C'] != None:
                    maps, prompt = format_prompt_4(d, args)
                else:
                    maps, prompt = format_prompt_2(d, args)
                
                system_prompt = ""
                if args.language == "zh":
                    if args.cot == False:
                        system_prompt = SystemEvaluatePrompt_zh
                    else:
                        system_prompt = SystemEvaluatePrompt_zh_cot
                else:
                    if args.cot == False:
                        system_prompt = SystemEvaluatePrompt_en
                    else:
                        system_prompt = SystemEvaluatePrompt_en_cot
                
                payload = {
                    "model": args.model_name,
                    "stream": False,
                    "top_p": 0.99,
                    "temperature": 0,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": prompt}
                    ],
                    "idx" : i,
                    "number" : j,
                    "data" : d, 
                    "map" : maps,
                    "answer" : d['答案\nANSWER'],
                    "save_path" : f"{args.output_path}/{task}_{args.model_name}_results.jsonl"
                }
                payloads.append(payload)

                
        with ThreadPoolExecutor(max_workers=32) as executor:
            for payload in payloads:
                executor.submit(processor.multiple_gpt, payload)
