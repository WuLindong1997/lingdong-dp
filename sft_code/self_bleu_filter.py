import concurrent.futures
import pandas as pd
import random
from nltk.translate.bleu_score import sentence_bleu, corpus_bleu
import nltk
import time
from tqdm import tqdm, trange
import json
import jieba

random.seed(66)

with open('/pretrain-data-bucket/sft_data/ape210k/train.ape.json', encoding='utf-8') as f:
    all_data = f.readlines()
    data = list(map(json.loads,all_data))

random.shuffle(data)


num_parts = 4
part_size = len(data) // num_parts + 1
parts = [data[i:i + part_size] for i in range(0, len(data), part_size)]


tokenizer = nltk.word_tokenize

if_english = False


def chinese_tokenize(s):
    return list(s)


def process_data(data):
    # do your processing here
    ctx = []
    dialog = []

    for i in data:
        # text = i[0]
        text = i['dialog'][0]['input']+'\t'+i['dialog'][1]['output']
        ctx.append(text)
        dialog.append(i)

    context = ctx
    tmp_ctx = [ctx[0]]

    for i in trange(len(context)):
        if if_english:
            now_sen = tokenizer(str(context[i]))
        else:
            now_sen = chinese_tokenize(str(context[i]))
        # print(now_sen)
        refs = random.sample(tmp_ctx, min(len(tmp_ctx), 1000))
        # print(sentence_bleu(reference, now_sen))
        if sentence_bleu(refs, now_sen) < 0.25:
            # print(1)
            tmp_ctx.append(now_sen)
            with open('/mnt/vepfs/pretrain/sft_data/ape210k/train.ape.json', 'a', encoding='utf-8') as f:
                print(json.dumps(data[i], ensure_ascii=False), file=f)


with concurrent.futures.ProcessPoolExecutor() as executor:
    results = list(executor.map(process_data, parts))