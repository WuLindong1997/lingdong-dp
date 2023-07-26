import concurrent.futures
import pandas as pd
import random
from nltk.translate.bleu_score import sentence_bleu, corpus_bleu
import nltk
import time
from tqdm import tqdm, trange
import json
import jieba
import functools
import os
import argparse
import multiprocess
random.seed(66)

def get_args():
    args_parser = argparse.ArgumentParser(description='parse_html')

    # dictionary or file
    args_parser.add_argument('--dataset_path', type=str,default='/mnt/vepfs/Pretrain-data/wulindong/sft_data/OpenOrca_format')
    args_parser.add_argument('--save_path', type=str,default='/mnt/vepfs/Pretrain-data/wulindong/sft_data/OpenOrca_bleu')
    args_parser.add_argument('--pool_num', type=int,default = 50)

    # parse
    args = args_parser.parse_args()

    return args
def chinese_tokenize(s):
    return list(s)


def process_data(data,save_path):
    # do your processing here
    # data,save_path = arg
    ctx = []
    dialog = []
    for i in data:
        # text = i[0]
        text = i['dialog'][0]['input']
        # text = i['dialog'][0]['input']
        ctx.append(text)
        dialog.append(i)

    context = ctx
    tmp_ctx = [tokenizer(ctx[0])]

    for i in trange(len(context)):
        if if_english:
            now_sen = tokenizer(str(context[i]))
        else:
            now_sen = chinese_tokenize(str(context[i]))
        # print(now_sen)
        refs = random.sample(tmp_ctx, min(len(tmp_ctx), 2000))
        # print(sentence_bleu(reference, now_sen))
        if sentence_bleu(refs, now_sen) < 0.35:
            # print(1)
            tmp_ctx.append(now_sen)
            with open(save_path, 'a', encoding='utf-8') as f:
                f.write(json.dumps(data[i],ensure_ascii=False)+'\n')
def get_data(input_path):
    with open(input_path, encoding='utf-8') as f:
        all_data = f.readlines()
        data1 = []
        for line in all_data:
            try:
                data1.append(json.loads(line, strict=False))
            except json.JSONDecodeError:
                print(f'JSON format error: {line}')
                continue
        
        random.shuffle(data1)

    return data1


if __name__ == '__main__':
    args = get_args()
    root_path = args.dataset_path
    file_paths = []
    for root,dir,file_names in os.walk(root_path):
        for file_name in file_names:
            if file_name.endswith('.jsonl') and '100k-GPT4-AugmentedSmallSubmix-train' in file_name:
                file_paths.append(os.path.join(root,file_name))
    for path in file_paths:
        save_path = os.path.join(args.save_path,path.split('/')[-1])
        if os.path.exists(save_path):
            print(f'{save_path}\tskip!')
            continue
        data2 = get_data(path)
        num_parts = 20
        part_size = len(data2) // num_parts + 1
        parts = [data2[i:i + part_size] for i in range(0, len(data2), part_size)]

        tokenizer = nltk.word_tokenize

        if_english = True
        new_process_data = functools.partial(process_data, save_path = save_path)
        # with concurrent.futures.ProcessPoolExecutor(max_workers = args.pool_num) as executor:
        #     results = list(executor.map(new_process_data, parts))
        with multiprocess.Pool(args.pool_num) as pool:
            results = list(pool.map(new_process_data, parts))