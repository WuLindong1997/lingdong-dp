import argparse
from bs4 import BeautifulSoup
import json
import re
from tqdm import tqdm
import multiprocessing
import os
import random
import io

   

def get_args():
    args_parser = argparse.ArgumentParser(description='parse_html')

    # dictionary or file
    args_parser.add_argument('--dataset_path', type=str,default='/pretrain-data-bucket/pretrain_other/pretrain_else/xiaohongshu_save_emoji_end')
    args_parser.add_argument('--save_path', type=str,default='/mnt/lingxin/vepfs/pretrain/wulindong/xiaohongshu.json')
    args_parser.add_argument('--pool_num', type=int,default = 12)

    # parse
    args = args_parser.parse_args()

    return args



if __name__ == '__main__':
    # 1.args
    args = get_args()
    data_dir = '/pretrain-data-bucket/pretrain_other/pretrain_else/weixin_page_dudmp'
    json_files = []
    for root, dirs, files in os.walk(data_dir):
        for file in files:
            if file.endswith('.jsonl'):
                json_files.append(os.path.join(root, file))
    result = []
    for path in tqdm(json_files):
        try:
            with open(path,'r',encoding='utf-8')as file:
                all_data = file.read().split('\n')[:-1]
            length = len(all_data)
            get_data = [all_data[random.randint(0,length)] for i in range(2000)]
            for line in get_data:
                
                result.append(line)
        
        except:
            pass
    with open('/mnt/vepfs/lingxin/Pretrain-data/wulindong/sft_code','w',encoding='utf-8')as file1:
        data = '\n'.join(result)
        file1.write(data)
