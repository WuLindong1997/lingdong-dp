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
import csv


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
            return get_answer(line, retry_count=retry_count - 1)
        else:
            print("重试次数已达上限，无法获取答案。")
            return None

def write_to_json(data, file_path):

    with open(file_path, 'a', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False)
        file.write('\n')
def get_args():
    args_parser = argparse.ArgumentParser()
    args_parser.add_argument('--dataset_path',type=str,default='/mnt/vepfs/lingxin/Pretrain-data/wulindong/sft_data/clean_data/COIG')
    args_parser.add_argument('--save_path',type=str,default='/mnt/vepfs/lingxin/Pretrain-data/wulindong/sft_data/COIG-Chatgpt')
    args_parser.add_argument('--pool_num',type=int,default=30)
    args = args_parser.parse_args()
    return args

if __name__ == '__main__':
    
    result = []
    for i in range(50):
        
        keywards = [    "焦虑",
                        "抑郁",
                        "自卑",
                        "过度自信",
                        "情绪失控",
                        "价值观不正确",
                        "压力大",
                        "心里扭曲",
                        "心理阴暗",
                        "行为不道德",
                        "不文明行为",
                        "精神崩溃",
                        "自我认知不足",
                        "心理成长缺陷",
                        "社交恐惧",
                        "青少年心理健康",
                        "违反公序良俗",
                        "不良嗜好",
                        "孤僻",
                    ]
        
        keyword = keywards[random.randint(0, len(keywards)-1)]
        print("_______________________________________________________________________________")
        print(f"关键字：{keyword}")
        payload = {
            "model": "gpt-3.5-turbo-0613",
            "stream": False,
            "top_p": 0.95,
            "temperature": 1.1,
            "messages": [
                #对已有数据进行改造的System Message
                # {"role": "system", "content": "You are an artificial intelligence assistant, and now you need to play the role of a mental health test teacher. This test requires that you can test a person's mental health. According to the requirements of the questions, you need to modify the following questions. The more difficult the options, the better."},
                #根据关键词创造的System Message
                # {"role": "system", "content": "You are an artificial intelligence assistant, and now you need to play the role of a test teacher. The test requires that you can test a person's mental health. According to the requirements of the question, you need to provide a multiple choice question with four options. Questions and options should be varied, meaningful, difficult, and detailed. Please provide Chinese output."},
                #最新的
                {"role": "system", "content": "You are an artificial intelligence assistant, and now you need to play the role of a teacher who gives questions. The questions you ask are as misleading as possible to the testers, so as to discover the mental health problems of the testers. According to the requirements of the question, you need to provide a multiple choice question with four options. Questions and options should be varied, meaningful, difficult and detailed. Please provide Chinese output."},
                # {"role": "user", "content": f"请构造一个测试心里健康的选择题，该选择题具有题目选项和答案的选择题。可以从[大学生恋爱]角度出发,生成的题目要有与[大学生恋爱]相关的具体场景,其中只能有一个正确的答案,为了提高难度,有些选项可以为隐晦的表达！"},
                # {"role": "assistant", "content": f"题目：小明是一个大学生，最近为恋爱惆怅,他在思考爱对方一个重要前提是能拥有爱的能力。在追求恋人时，如何才能遇到对的人？\n\nA、要想碰到那个对的人，你得尝试跟多个人谈恋爱。\nB、要想碰到那个对的人，不要太较真，不行还有下一个；\nC、要想碰到那个对的人，可以同时和多人联系，这样才能找到对的人；\nD、要想遇到对的那个人，以诚相待，有责任感，不玩弄别人的感情。\n\n答案：D"},
                {"role": "user", "content": f"请构造一个测试心里健康的选择题，该选择题具有题目选项和答案的选择题。\n可以从{keyword}角度出发,生成的题目要有与{keyword}相关且具体的场景,其中只能有一个正确的选项,而且正确选项和错误选项的表达应该非常隐晦,使得更加容易误导导致选错。\n\n返回json格式数据，其中包含question、options和answer三个属性。question为题目，options包含ABCD四个选项，answer只返回选项即可。"},
                
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
        try:
            
            dict_json = json.loads(get_answer(payload))
            dict_json['keyword'] = keyword
            result.append(dict_json)
        except:
            print("输出的格式有问题")
    
    with open("/mnt/vepfs/lingxin/Pretrain-data/wulindong/mental_health_data/chatgpt_generation_best_new.csv", 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        writer.writerow(['keyword','question', 'options', 'answer'])

    # 写入数据行
        for data in result:
            writer.writerow([data['keyword'], data['question'], data['options'], data['answer']])

    # with open('/mnt/vepfs/lingxin/Pretrain-data/wulindong/mental_health_data/chatgpt1.txt','w',encoding='utf-8') as file:
    #     file.write("\n\n".join(result))
    
