import json
import argparse
import os

def most_common_element(lst):
    element_freq = {}
    for item in lst:
        element_freq[item] = element_freq.get(item, 0) + 1
    most_common = max(element_freq, key=element_freq.get)
    return most_common


def extract_answer(text):
    if "[[A]]" in text:
        return "A"
    elif "[[B]]" in text:
        return "B"
    elif "[[C]]" in text:
        return "C"
    elif "[[D]]" in text:
        return "D"
    elif "[A]" in text:
        return "A"
    elif "[B]" in text:
        return "B"
    elif "[C]" in text:
        return "C"
    elif "[D]" in text:
        return "D"
    else:
        for i in range(len(text) - 1, -1, -1):
            if text[i] == 'A':
                return "A"
            elif text[i] == 'B':
                return "B"
            elif text[i] == 'C':
                return "C"
            elif text[i] == 'D':
                return "D"
    return "A"


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_path", type=str, default="")
    parser.add_argument("--try_times", type=int, default=5)
    args = parser.parse_args()
    
    files = os.listdir("./results")
    acc_per_task = {}
    cnt_per_task = {}

    acc_per_ability = {}
    cnt_per_ability = {}
    
    for file in files:
        with open(f"./results/{file}", "r", encoding='utf-8') as f:
            data = [json.loads(line) for line in f.readlines()]
        
        answers = ["" for _ in range(len(data) // args.try_times)]
        preds = [[] for _ in range(len(data) // args.try_times)]
        abilities = ["" for _ in range(len(data) // args.try_times)]
        for d in data:
            preds[d['idx']].append(d['map'][extract_answer(d['output'])])
            if answers[d['idx']] == "":
                answers[d['idx']] = d['answer']
            
            if abilities[d['idx']] == "":
                abilities[d['idx']] = d['data']['能力\nABILITY']
        

        for i in range(len(data) // args.try_times):
            task = file.split("_")[0]
            ability = abilities[i]

            cnt_per_task[task] = cnt_per_task.get(task, 0) + 1
            cnt_per_ability[ability] = cnt_per_ability.get(ability, 0) + 1


            if answers[i] == most_common_element(preds[i]):
                acc_per_task[task] = acc_per_task.get(task, 0) + 1
                acc_per_ability[ability] = acc_per_ability.get(ability, 0) + 1
    
    for task in acc_per_task.keys():
        acc_per_task[task] /= cnt_per_task[task]
    
    for ability in acc_per_ability.keys():
        acc_per_ability[ability] /= cnt_per_ability[ability]
    
    results = {
        "tasks" : acc_per_task,
        "abilities" : acc_per_ability
    }

    with open("results.json", "w", encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=4)
            