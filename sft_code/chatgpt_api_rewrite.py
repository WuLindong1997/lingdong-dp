# -*- coding: utf-8 -*-

import sys
import json
import os
import time
import requests
from openpyxl import load_workbook
from tqdm import tqdm, trange
from concurrent.futures import ThreadPoolExecutor
import multiprocessing
import argparse
import random
import pandas as pd


def read_jsonl(input_file: str) -> list:
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    return list(map(json.loads, tqdm(lines, desc='Reading...')))

def get_answer(line,retry_count = 3):
    payload = line
    
    #公司的key
    url = "https://api.openai-sb.com/v1/chat/completions"
    headers = {
        #个人的key
        #"Authorization": "Bearer sb-1c9d8211cdbac8c808ba47226b7790f92c348b4e0e4ed2de",
        
        #公司的key
        "Authorization": "Bearer sb-c1846034d6d59562cfb8124f7b383d280db3f249c58bda1d",
        "Content-Type": "application/json"
    }

    try:
        #请求访问接口
        response = requests.post(url, json=payload, headers=headers).json()
        #取出回复获取答案
        answer = response['choices'][0]['message']['content']
        print(answer)
        #放入在data数据中加入获得的答案字段
        return answer


    except Exception as e:
        print("发生了异常:", str(e))
        if retry_count > 0:
            print("等待0.2秒后进行重试...")
            time.sleep(0.2)
            return json.loads(get_answer(line, retry_count=retry_count - 1))
        else:
            print("重试次数已达上限，无法获取答案。")
            return None

def write_to_json(data, file_path):

    with open(file_path, 'a', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False)
        file.write('\n')
def get_args():
    args_parser = argparse.ArgumentParser()
    args_parser.add_argument('--dataset_path',type=str,default='/mnt/vepfs/lingxin/Pretrain-data/wulindong/mental_health_data/身心健康1.csv')
    args_parser.add_argument('--save_path',type=str,default='/mnt/vepfs/lingxin/Pretrain-data/wulindong/sft_data/COIG-Chatgpt')
    args_parser.add_argument('--pool_num',type=int,default=30)
    args = args_parser.parse_args()
    return args

if __name__ == '__main__':
    args = get_args()
    
    df = pd.read_csv(args.dataset_path)
    result = []
    for index, row in df.iterrows():
    # 在这里对每一行进行处理
        question = row[0]
        options = row[1]
        answer = row[2]
        print("_______________________________________________________________________________")
        
        payload = {
            "model": "gpt-3.5-turbo-0613",
            "stream": False,
            "top_p": 0.99,
            "temperature": 1.5,
            "messages": [
                #对已有数据进行改造的System Message
                {"role": "system", "content": "You are an artificial intelligence assistant, and now you need to play the role of a mental health test teacher. This test requires that you can test a person's mental health. According to the requirements of the questions, you need to modify the following questions. The more difficult the options, the better."},
                #根据关键词创造的System Message
                # {"role": "system", "content": "You are an artificial intelligence assistant, and now you need to play the role of a test teacher. The test requires that you can test a person's mental health. According to the requirements of the question, you need to provide a multiple choice question with four options. Questions and options should be varied, meaningful, difficult, and detailed. Please provide Chinese output."},
                # {"role": "user", "content": f"请构造一个测试心里健康的选择题，该选择题具有题目选项和答案的选择题。可以从[大学生恋爱]角度出发,生成的题目要有与[大学生恋爱]相关的具体场景,其中只能有一个正确的答案,为了提高难度,有些选项可以为隐晦的表达！"},
                # {"role": "assistant", "content": f"题目：小明是一个大学生，最近为恋爱惆怅,他在思考爱对方一个重要前提是能拥有爱的能力。在追求恋人时，如何才能遇到对的人？\n\nA、要想碰到那个对的人，你得尝试跟多个人谈恋爱。\nB、要想碰到那个对的人，不要太较真，不行还有下一个；\nC、要想碰到那个对的人，可以同时和多人联系，这样才能找到对的人；\nD、要想遇到对的那个人，以诚相待，有责任感，不玩弄别人的感情。\n\n答案：D"},
                {"role": "user", "content": f"请修改一个测试心里健康的选择题，该选择题具有题目选项和答案的选择题。\n\nquestios:{question}\n\noptions:{options}\n\nanswer:{answer},\n\n修改要求：\n其中只能有一个正确的选项,其余三个错误选项的表达应该非常隐晦(如果是不到四个选项的拓展选项),使得更加容易误导导致选错。\n\n返回json格式数据，其中包含question、options和answer三个属性。question为题目，options包含ABCD四个选项，answer只返回选项即可。"},
                
            ]
        }
            #可以修改prompt
        

            #整理好的数据放入接口进行处理
            #多线程
            # lock = multiprocessing.Lock()
            # with ThreadPoolExecutor(max_workers=8) as executor:
            #     for payload in tqdm(payloads):
            #         executor.submit(get_answer, *payload)

            #多进程
            # lock = multiprocessing.Lock()
        result.append(json.dumps(get_answer(payload),ensure_ascii=False))
    with open('/mnt/vepfs/lingxin/Pretrain-data/wulindong/mental_health_data/chatgpt_generation.json','w',encoding='utf-8')as file:
        file.write("["+'\n'.join(result).strip(',')+"]")

    # with open('/mnt/vepfs/lingxin/Pretrain-data/wulindong/mental_health_data/chatgpt1.txt','w',encoding='utf-8') as file:
    #     file.write("\n\n".join(result))
    
