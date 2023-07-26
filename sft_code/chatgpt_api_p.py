"""
    @Time    : 2023/6/27 15:34
    @Author  : LindongWu
    @Email   : wldsty@126.com
    @File    : chatgpt_api.py
"""
# -*- coding: utf-8 -*-

import sys
import json
import os
import time
import requests
from tqdm import tqdm, trange
import multiprocessing
import argparse


def read_jsonl(input_file: str) -> list:
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    return list(map(json.loads, tqdm(lines, desc='Reading...')))


def get_answer(line, retry_count=3):
    payload, data, save_path = line[0], line[1], line[2]

    # 公司的key
    url = "https://api.openai-sb.com/v1/chat/completions"
    headers = {
        # 个人的key
        # "Authorization": "Bearer sb-1c9d8211cdbac8c808ba47226b7790f92c348b4e0e4ed2de",

        # 公司的key
        "Authorization": "Bearer sb-c1846034d6d59562cfb8124f7b383d280db3f249c58bda1d",
        "Content-Type": "application/json"
    }

    try:
        # 请求访问接口
        response = requests.post(url, json=payload, headers=headers).json()
        # 取出回复获取答案
        answer = response['choices'][0]['message']['content']

        # 放入在data数据中加入获得的答案字段
        data['chatgpt'] = answer

    except Exception as e:
        print("发生了异常:", str(e))
        if retry_count > 0:
            print("等待5秒后进行重试...")
            time.sleep(2)
            return get_answer(line, retry_count=retry_count - 1)
        else:
            print("重试次数已达上限，无法获取答案。")
            return None
    write_to_json(data, save_path)


def write_to_json(data, file_path):
    with open(file_path, 'a', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False)
        file.write('\n')


def get_args():
    args_parser = argparse.ArgumentParser()
    args_parser.add_argument('--dataset_path', type=str,
                             default='/mnt/vepfs/lingxin/Pretrain-data/wulindong/sft_data/poetry_raw')
    args_parser.add_argument('--save_path', type=str,
                             default='/mnt/vepfs/lingxin/Pretrain-data/wulindong/sft_data/poetry_chatgpt')
    args_parser.add_argument('--pool_num', type=int, default=30)
    args = args_parser.parse_args()
    return args


if __name__ == '__main__':

    args = get_args()
    # 加载数据文件路径
    input_files = []
    output_files = []
    for root, dirs, files in os.walk(args.dataset_path):
        for file in files:
            if file.endswith(".json") and "poem_train.js" in file:
                input_files.append(os.path.join(root, file))
                output_files.append(os.path.join(args.save_path, file))

    for file_path, save_path in zip(input_files, output_files):
        # 读取文件,将数据转化为prompt
        datas = read_jsonl(file_path)
        payloads = []
        for data in tqdm(datas):
            payload = {
                "model": "gpt-3.5-turbo-0613",
                "stream": False,
                "top_p": 0.95,
                "temperature": 1,
                "messages": [
                    {"role": "user", "content": "树上有9只鸟，猎人开枪打死1只，树上还剩几只鸟?"}
                ]
            }
            prompt = '根据下面提供的诗歌信息，给出简短的主题大意。'
            # 可以修改prompt
            payload['messages'][0]['content'] = f'{prompt}\n\n{data["prompt"]}\n{data["answer"]}\n'
            payloads.append([payload, data, save_path])

        # 整理好的数据放入接口进行处理
        # 多线程
        # lock = multiprocessing.Lock()
        # with ThreadPoolExecutor(max_workers=8) as executor:
        #     for payload in tqdm(payloads):
        #         executor.submit(get_answer, *payload)

        # 多进程
        # lock = multiprocessing.Lock()
        with multiprocessing.Pool(args.pool_num) as pool:
            pool.map(get_answer, payloads)

