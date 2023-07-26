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
        data = line['raw']
        data = json.loads(data, strict=False)
        liked_count = data['liked_count']
        collected_count = data['collected_count']
        title = data['title']
        desc = data['desc']
        text_dic = {}
        text_dic['text'] =title+'\n'+desc
        text_dic['liked_count'] = liked_count
        text_dic['collected_count'] = collected_count

        json_str_cn = json.dumps(text_dic, ensure_ascii=False)
        return json_str_cn
    except:
        text_dic = {}
        text_dic['text'] =''
        text_dic['liked_count'] = 0
        text_dic['collected_count'] = 0
        print('有问题')
        json_str_cn = json.dumps(text_dic, ensure_ascii=False)
        return json_str_cn

def trans_data(path):
    with open(path,'r',encoding='utf-8') as file:
        lines = file.read().split('\n')
    result = []
    with multiprocessing.Pool(10) as pool:
        result = list(tqdm(pool.imap(get_json, lines), total=len(lines)))
    
    with open(args.save_path, 'w', encoding='utf-8') as file:
        file.write('\n'.join(result[:-1]))

def get_args():
    parser = argparse.ArgumentParser("clean xiaohongshu data")
    parser.add_argument('--data_path',type=str,default= '/mnt/vepfs/lingxin/pretrain/wulindong/xhs_notes.2019-12-27')
    parser.add_argument('--save_path',type=str,default= '/mnt/vepfs/lingxin/pretrain/wulindong/xhs_notes.2019-12-27.json')
    return parser.parse_args()


if __name__ == '__main__':
    args = get_args()
    trans_data(args.data_path)