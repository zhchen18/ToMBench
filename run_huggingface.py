import json
import random
from transformers import AutoModelForCausalLM, AutoTokenizer
import argparse
from prompts import *
from tqdm import tqdm
import os


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
    parser.add_argument("--language", type=str, default="zh")
    parser.add_argument("--try_times", type=int, default=5)
    parser.add_argument("--cot", type=bool, default=False)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    random.seed(args.seed)

    tokenizer = AutoTokenizer.from_pretrained(args.model_name, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(args.model_name, trust_remote_code=True).half().cuda()

    model_name = args.model_name.split("/")[-1]
    
    files = os.listdir("./data")
    if args.task != "":
        files = [args.task]
    
    for file in files:
        task = file.split(".")[0]
        with open(f"data/{file}", "r", encoding='utf-8') as f:
            data = [json.loads(line) for line in f.readlines()]
        
        print(file)
        for i, d in tqdm(enumerate(data[:10])):
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

                messages = [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ]
                gen_kwargs = {"max_length": 4096, "do_sample": False, "top_k": 1}
                inputs = tokenizer.apply_chat_template(messages, return_tensors="pt", tokenize=True, return_dict=True)
                inputs = inputs.to(model.device)
                outputs = model.generate(**inputs, **gen_kwargs)
                outputs = outputs[:, inputs['input_ids'].shape[1]:]
                outputs = tokenizer.decode(outputs[0], skip_special_tokens=True)
                out = {}
                out['idx'] = i
                out['number'] = j
                out['answer'] = d['答案\nANSWER']
                out['map'] = maps
                out['data'] = d
                out['output'] = outputs

                with open(f"./results/{task}_{model_name}_results.jsonl", "a+", encoding='utf-8') as f:
                    f.write(json.dumps(out, ensure_ascii=False) + "\n")
