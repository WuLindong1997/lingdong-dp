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
    args_parser.add_argument('--dataset_path', type=str,default='/mnt/vepfs/lingxin/Pretrain-data/wulindong/sft_data/codealpaca/rosetta_alpaca.json')
    args_parser.add_argument('--save_path', type=str,default='/mnt/vepfs/lingxin/Pretrain-data/wulindong/sft_data/codealpaca_format/rosetta_alpaca.json')
    args_parser.add_argument('--pool_num', type=int,default = 12)
    # parse
    args = args_parser.parse_args()
    return args

if __name__ == '__main__':
    args = get_args()
    # json_files = []
    # for root, dirs, files in os.walk(args.dataset_path):
    #     for file in files:
    #         if file.endswith('.json'):
    #             json_files.append(os.path.join(root, file))
    # result = []
    
    # file_name_path = os.path.join(args.save_path,path.split('/')[-2])
    # save_path = os.path.join(args.save_path,path.split('/')[-1])
    result = []
    with open(args.dataset_path,'r',encoding='utf-8')as file:
        all_data = file.read()
        all_data = json.loads(all_data)
        for line in all_data:
            if line[INPUT] == '':
                # if 'xxx' in line[INSTRUCTION]:
                #     continue
                # pattern = r'^\d+\.|^\d+.'
                # pattern1 = r'\t{2,}'
                # input = {'input':re.sub(r'\t{2,}', '\t', line[INSTRUCTION])}
                input = {'input':line[INSTRUCTION]}
            else:
                # if 'xxx' in line[INSTRUCTION]+line[INPUT]:
                #     continue
                # input = {'input':re.sub(pattern)+'\n'+line[INPUT]}
                # input = {'input':re.sub(r'\t{2,}', '\t', line[INSTRUCTION]+'\n'+line[INPUT])}
                input = {'input':line[INSTRUCTION]+'\n'+line[INPUT]}
            output = {'output':line[OUTPUT]}
            dialog = [input,output]
            result.append(json.dumps({'type':['code',{"dataset_name":"code_alpaca"}],'dialog':dialog},ensure_ascii=False))
        
    with open(args.save_path,'w',encoding='utf-8')as file1:
        file1.write('\n'.join(result))