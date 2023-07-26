#提取原始数据
#数据格式为：{input:'' , output:''}
import os
import json
import argparse
import ast
from tqdm import tqdm

INSTRUCTION = 'original_text'
INPUT = 'input'
OUTPUT = 'equation'


def get_args():
    args_parser = argparse.ArgumentParser()
    # dictionary or file
    args_parser.add_argument('--dataset_path', type=str,default='/mnt/vepfs/lingxin/Pretrain-data/wulindong/sft_data/RefGPT')
    args_parser.add_argument('--save_path', type=str,default='/mnt/vepfs/lingxin/Pretrain-data/wulindong/sft_data/RefGPT_format')
    args_parser.add_argument('--pool_num', type=int,default = 12)
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
    # result = []
    for path in json_files: 
        save_path = os.path.join(args.save_path,path.split('/')[-1])
        result = []
        with open(path,'r',encoding='utf-8')as file:
            # all_data = file.read().replace(r'\\n', '\\n')
            
            all_data = json.loads(file.read())

            for line in tqdm(all_data):
                # if line[INPUT] == '':
                #     input = {'input':line[INSTRUCTION]}
                # else:
                #     input = {'input':line[INSTRUCTION]+'\n'+line[INPUT]}
                batch_size = 2
                start = 0
                line = line['content']
                result1 = []
                try:
                    while start < len(line):
                        input = {'input':line[start]}
                        output = {'output':line[start+1]}
                        start+=batch_size
                        result1.append(input)
                        result1.append(output)
                    # output = {'output':line[OUTPUT]+'\n'+line['ans']}
                    dialog = result1
                    result.append(json.dumps({'type':['参考对话',{"dataset_name":"RefGPT"}],'dialog':dialog},ensure_ascii=False))
                except:
                    print("有错误！")
        if os.path.exists(args.save_path):
            with open(save_path,'w',encoding='utf-8')as file1:
                file1.write('\n'.join(result))
        else:
            os.mkdir(args.save_path)
            with open(save_path,'w',encoding='utf-8')as file1:
                file1.write('\n'.join(result)) 