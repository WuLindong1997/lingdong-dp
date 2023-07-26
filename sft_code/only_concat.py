#提取原始数据
#数据格式为：{input:'' , output:''}
import os
import json
import argparse
import ast

INSTRUCTION = 'original_text'
INPUT = 'input'
OUTPUT = 'equation'


# def get_args():
#     args_parser = argparse.ArgumentParser()
#     # dictionary or file
#     args_parser.add_argument('--dataset_path', type=str,default='/mnt/vepfs/lingxin/Pretrain-data/wulindong/sft_data/Chain-of-Thought')
#     args_parser.add_argument('--save_path', type=str,default='/mnt/vepfs/lingxin/Pretrain-data/wulindong/sft_data/Chain-of-Thought_format')
#     args_parser.add_argument('--pool_num', type=int,default = 12)
#     # parse
#     args = args_parser.parse_args()
#     return args

if __name__ == '__main__':
    # args = get_args()

    path1 = '/mnt/vepfs/lingxin/Pretrain-data/wulindong/sft_data/Chain-of-Thought/formatted_cot_data'
    path2 = '/mnt/vepfs/lingxin/Pretrain-data/wulindong/sft_data/Chain-of-Thought/formatted_cot_data_Chinese'
    save_path = '/mnt/vepfs/lingxin/Pretrain-data/wulindong/sft_data/Chain-of-Thought_format'
    en_paths = os.listdir(path1)
    zh_paths = os.listdir(path2)

    for en_path,zh_path in en_paths,zh_paths: 
        save_path = os.path.join(save_path,en_path)
        result = []
        with open(en_path,'r',encoding='utf-8')as file:
            en_all_data = file.read().replace(r'\\n', '\\n').split('\n')
            
        with open(zh_path,'r',encoding='utf-8')as file1:
            zh_all_data = file1.read().replace(r'\\n', '\\n').split('\n')

        for en_line,zh_line in en_all_data,zh_all_data:
            '''
            {
                en:{input:  ,}


            }
            '''
            input = {'input':en_line[INSTRUCTION]}
            output = {'output':en_line[OUTPUT]+'\n'+en_line['ans']}
            dialog = [input,output]
            result.append(json.dumps({'type':['数学',{"dataset_name":"Math23k"}],'dialog':dialog},ensure_ascii=False))
            
        with open(save_path,'w',encoding='utf-8')as file1:
            file1.write('\n'.join(result))     