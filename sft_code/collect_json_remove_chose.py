#提取原始数据
#数据格式为：{input:'' , output:''}
import os
import json
import argparse
import ast

INSTRUCTION = 'instruction'
INPUT = 'input'
OUTPUT = 'output'


def get_args():
    args_parser = argparse.ArgumentParser()
    # dictionary or file
    args_parser.add_argument('--dataset_path', type=str,default='/mnt/vepfs/lingxin/Pretrain-data/wulindong/sft_data/clean_data/COIG')
    args_parser.add_argument('--save_path', type=str,default='/mnt/vepfs/lingxin/Pretrain-data/wulindong/sft_data/clean_data/COIG_end')
    args_parser.add_argument('--pool_num', type=int,default = 12)
    # parse
    args = args_parser.parse_args()
    return args

if __name__ == '__main__':
    args = get_args()
    json_files = []
    for root, dirs, files in os.walk(args.dataset_path):
        for file in files:
            if file.endswith('.json'):
                json_files.append(os.path.join(root, file))
    # result = []
    for path in json_files: 
        save_path = os.path.join(args.save_path,path.split('/')[-1])
        result = []
        with open(path,'r',encoding='utf-8')as file:
            # all_data = file.read()
            data_a = file.readlines()
            # all_data = json.loads(all_data)
            all_data = list(map(json.loads,data_a))
            # all_data = json.loads(file.read())

        for line in all_data:
            if '选择' in line['dialog'][0]["input"]:
                if 'A' in line['dialog'][0]["input"]:
                    result.append(json.dumps(line,ensure_ascii=False))
                else:
                    pass
            else:
                result.append(json.dumps(line,ensure_ascii=False))

        
        with open(save_path,'w',encoding='utf-8')as file1:
            file1.write('\n'.join(result)) 