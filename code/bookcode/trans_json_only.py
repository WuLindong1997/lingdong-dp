#提取原始数据
#数据格式为：{input:'' , output:''}
import os
import json
import argparse
import ast



def get_args():
    args_parser = argparse.ArgumentParser()
    # dictionary or file
    args_parser.add_argument('--dataset_path', type=str,default='/mnt/vepfs/lingxin/Pretrain-data/wulindong/code/bookcode/清洗-stage1/outputs_part2/中国哲学史')
    args_parser.add_argument('--save_path', type=str,default='/mnt/vepfs/lingxin/Pretrain-data/wulindong/code/bookcode/bookdata_clean/book_json_part2/中国哲学史.json')
    args_parser.add_argument('--pool_num', type=int,default = 30)
    # parse
    args = args_parser.parse_args()
    return args


if __name__ == '__main__':
    args = get_args()
    
    dataset_path = args.dataset_path
    save_path = args.save_path
    result = []
    with open(dataset_path,'r',encoding='utf-8')as file:
        # all_data = file.read().replace(r'\\n', '\\n')
        
        all_data = file.read()
        all_data = all_data.split('\n')
    for line in all_data:
        line  = line.strip()
        if len(line)> 0:
            json_line = json.dumps({'text':line},ensure_ascii=False)         
            result.append(json_line)
    # with open(save_path,'w',encoding='utf-8')as file1:
    #         file1.write('\n'.join(result))
    with open(save_path,'w',encoding='utf-8')as file1:
        file1.write('\n'.join(result)) 