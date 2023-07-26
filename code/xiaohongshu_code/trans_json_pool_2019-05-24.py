import argparse
import json
import ast
import multiprocessing
import re

from tqdm import tqdm

def get_json(line):
    try:
        idx = line.find('{')
        line = line[idx:]
        line = line.strip('\t')
        # print(line)
        # line = ast.literal_eval(line)
        line = json.loads(line, strict=False)
        line = json.loads(line['raw'])
        liked_count = line['liked_count']
        collected_count = line['collected_count']
        title = line['title']
        desc = line['desc']
        text_dic = {}
        text = title+'\n'+desc
        text_dic['text'] =text.strip('\n')
        text_dic['liked_count'] = liked_count
        text_dic['collected_count'] = collected_count
        if '赞R' in text:
            print(line)
    
        json_str_cn = json.dumps(text_dic, ensure_ascii=False)
        return json_str_cn
        
    except:
        print('格式有误')
        
        return None
        

def trans_data(path):
    with open(path,'r',encoding='utf-8') as file:
        lines = file.read().split('\n')
    result = []
    with multiprocessing.Pool(10) as pool:
        result = list(tqdm(pool.imap(get_json, lines), total=len(lines)))
   
    with open(args.save_path, 'w', encoding='utf-8') as file:
        # for re
        # file.write('\n'.join(result[:-1]))
        result1 = []
        for line in result:
            if line is not None:
                result1.append(line)
        file.write('\n'.join(result1))
                

def get_args():
    parser = argparse.ArgumentParser("clean xiaohongshu data")
    parser.add_argument('--data_path',type=str,default= '/mnt/vepfs/lingxin/pretrain/wulindong/code/xiaohongshu_code/xhs_notes.2019-08-27')
    parser.add_argument('--save_path',type=str,default= './3.json')
    return parser.parse_args()


if __name__ == '__main__':
    args = get_args()
    trans_data(args.data_path)