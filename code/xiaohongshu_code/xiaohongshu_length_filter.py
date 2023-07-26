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
    data_dir = '/pretrain-data-bucket/pretrain_other/pretrain_else/xiaohongshu_save_emoji_end'
    save_dir = '/pretrain-data-bucket/pretrain_other/pretrain_else/xiaohongshu_save_emoji_length_end'
    json_files = []
    for root, dirs, files in os.walk(data_dir):
        for file in files:
            if file.endswith('.json'):
                json_files.append(os.path.join(root, file))
    result = []
    for path in tqdm(json_files):
        result = []
        with open(path,'r',encoding='utf-8')as file:
            all_data = file.read().split('\n')
        for line in all_data:
            json_line = json.loads(line)
            temp = re.sub(r'\[EMJ_START\].*?\[EMJ_END\]','',json_line['text'])
            if len(temp)<25:
                continue
            else:
                result.append(json.dumps(json_line,ensure_ascii=False))
        #保存地址
        file_name = path.split('\\')[-1]
        save_path = os.path.join(save_dir,file_name)
        
        #保存过滤后的数据
        with open(save_path,'w',encoding='utf-8')as file_save:
            file_save.write('\n'.join(result))
        
            
        
        
    with open('/mnt/vepfs/lingxin/pretrain/wulindong/weixin_page/code/clean_weixin/baike_sample.json','w',encoding='utf-8')as file1:
        data = '\n'.join(result)
        file1.write(data)
