#提取原始数据
#数据格式为：{input:'' , output:''}
import os
import json
import argparse
import ast
import re

INSTRUCTION = 'instruction'
INPUT = 'input'
OUTPUT = 'output'


def get_args():
    args_parser = argparse.ArgumentParser()
    # dictionary or file
    args_parser.add_argument('--dataset_path', type=str,default='/mnt/vepfs/lingxin/Pretrain-data/wulindong/sft_data/belle_cn_format/school_math_0.25M.json')
    args_parser.add_argument('--save_path', type=str,default='/mnt/vepfs/lingxin/Pretrain-data/wulindong/sft_data/belle_cn_format/school_math_0.25M.json')
    args_parser.add_argument('--name', type=str,default='belle_cn')
    # parse
    args = args_parser.parse_args()
    return args

if __name__ == '__main__':
    args = get_args()
    args.name = 'firefly'
    args.dataset_path = '/mnt/vepfs/lingxin/Pretrain-data/wulindong/sft_data/belle_cn_format/school_math_0.25M.json'
    args.save_path = '/mnt/vepfs/lingxin/Pretrain-data/wulindong/sft_data/belle_cn_format/school_math_0.25M1.json'

    result = []
    with open(args.dataset_path,'r',encoding='utf-8')as file:
        all_data = file.readlines()
        all_data = list(map(json.loads,all_data))
        result = []
        for line in all_data:
            line['type'].append({"dataset_name":args.name})
            result.append(json.dumps(line,ensure_ascii=False))
        
    with open(args.save_path,'w',encoding='utf-8')as file1:
        file1.write('\n'.join(result))