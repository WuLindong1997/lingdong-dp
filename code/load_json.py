#提取原始数据
#数据格式为：{input:'' , output:''}
import os
import json
import argparse
import ast
from tqdm import tqdm



def get_args():
    args_parser = argparse.ArgumentParser()
    # dictionary or file
    args_parser.add_argument('--dataset_path', type=str,default='/pretrain-data-bucket/pretrain_other/pretrain_else/weixin_page_end')
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
    result = []
    for path in tqdm(json_files): 
        with open(path,'r',encoding='utf-8')as file:
            all_data = file.readlines()
        flage = 1
        for line in tqdm(all_data):
            
            try:
                line  = json.loads(line)
                pass
            except Exception as e:
                print("An error occurred: ", e)
                print(f"path:{path}")
                print(f"content:{line}")
                flage = 0
            
        if flage == 1:
            result.append(path+'\tTrue')
        else:
            result.append(path+'\tFalse')
    with open('/mnt/vepfs/lingxin/Pretrain-data/wulindong/code/logs','w',encoding='utf-8')as file1:
        file1.write('\n'.join(result))