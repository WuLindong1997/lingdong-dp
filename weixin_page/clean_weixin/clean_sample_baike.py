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
    args_parser.add_argument('--dataset_path', type=str,default='/mnt/vepfs/lingxin/pretrain/wulindong/weixin_page.2015-06-21')
    args_parser.add_argument('--save_path', type=str,default='/mnt/vepfs/lingxin/pretrain/wulindong/test.json')
    args_parser.add_argument('--pool_num', type=int,default = 12)

    # parse
    args = args_parser.parse_args()

    return args



if __name__ == '__main__':
    # 1.args
    args = get_args()
    data_dir = '/pretrain-data-bucket/pretrain/clean_baike_end'
    json_files = []
    for root, dirs, files in os.walk(data_dir):
        for file in files:
            if file.endswith('.json'):
                json_files.append(os.path.join(root, file))
    result = []
    for path in tqdm(json_files[:1100]):
        try:
            with open(path,'r',encoding='utf-8')as file:
                all_data = file.read().split('\n')[:-1]
            length = len(all_data)
            get_data = [all_data[random.randint(0,length)]]
            if len(get_data[0])<20:
                continue
            result+=get_data
        
        except:
            pass
    with open('/mnt/vepfs/lingxin/pretrain/wulindong/weixin_page/code/clean_weixin/baike_sample.json','w',encoding='utf-8')as file1:
        data = '\n'.join(result)
        file1.write(data)
