import argparse
import json
import ast
import re
from tqdm import tqdm


def trans_data(path):
    with open(path,'r',encoding='utf-8') as file:
        lines = file.read().split('\n')
    result = []
    for line in tqdm(lines):
        if line == '':
            continue
        line = line.split('\t')[-1]
        # print(line)
        line = ast.literal_eval(line)
        line = json.loads(line['raw'], strict=False)
        liked_count = line['data'][0]['note_list'][0]['liked_count']
        collected_count = line['data'][0]['note_list'][0]['collected_count']
        title = line['data'][0]['note_list'][0]['title']
        desc = line['data'][0]['note_list'][0]['desc']
        text_dic = {}
        text_dic['text'] =title+'\n'+desc
        text_dic['liked_count'] = liked_count
        text_dic['collected_count'] = collected_count

        json_str_cn = json.dumps(text_dic, ensure_ascii=False)
        result.append(json_str_cn)
    with open(args.save_path, 'w', encoding='utf-8') as file:
        file.write('\n'.join(result))

def get_args():
    parser = argparse.ArgumentParser("clean xiaohongshu data")
    parser.add_argument('--data_path',type=str,default= '/mnt/vepfs/lingxin/pretrain/wulindong/xhs_notes.2021-01-01')
    parser.add_argument('--save_path',type=str,default= '/mnt/vepfs/lingxin/pretrain/wulindong/xhs_notes.2021-01-01.json')
    return parser.parse_args()


if __name__ == '__main__':
    args = get_args()
    trans_data(args.data_path)