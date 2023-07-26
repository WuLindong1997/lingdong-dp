import argparse
import json
import ast
import re
import emoji
import os
from time import time

def get_data(data_path):
    with open(data_path,'r',encoding='utf-8') as file:
        list_text = file.read().split('\n')
    return list_text


def re_clean(line):
    json_text = json.loads(line)
    text = json_text['text'] 

    str_text = json.dumps(json_text,ensure_ascii=False)
    return str_text,len(text)

def get_args():
    parser = argparse.ArgumentParser("clean xiaohongshu data")
    parser.add_argument('--data_path',type=str,default= '/pretrain-data-bucket/pretrain_other/pretrain_else/xiaohongshu_save_emoji_temp')
    parser.add_argument('--save_path',type=str,default= '/pretrain-data-bucket/pretrain_other/pretrain_else/xiaohongshu_save_emoji_end')
    return parser.parse_args()

def main():
    args = get_args()
    for file_name in os.listdir(args.data_path):
        start_time = time()
        path = os.path.join(args.data_path,file_name)
        save_path = os.path.join(args.save_path,file_name)
        if os.path.exists(save_path):
            print(f'{save_path} exist so skip!')
            continue
        list_text = get_data(path)[:-1]
        raw_total = len(list_text)
        result = []
        try:
            for line in list_text:
                
                text,length = re_clean(line)
                if length<25:  #为保证25个字符
                    continue
                result.append(text)
            clean_over_total = len(result)
            
            with open(save_path,'w',encoding='utf-8') as file:
                file.write('\n'.join(result))
            end_time = time()
            print(f'clean file:{file_name}\traw_total:{raw_total}\tclean_total:{clean_over_total}\tpercentage:{(clean_over_total/raw_total):.3f}%\ttime:{end_time-start_time}')
            
        except:
            print(f'{save_path} \t error')

if __name__ == '__main__':
    main()
