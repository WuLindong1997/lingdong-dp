#提取原始数据
#数据格式为：{input:'' , output:''}
import os
import json
import argparse
import ast

INSTRUCTION = 'original_text'
INPUT = 'input'
OUTPUT = 'equation'


def get_args():
    args_parser = argparse.ArgumentParser()
    # dictionary or file
    args_parser.add_argument('--dataset_path', type=str,default='/mnt/vepfs/lingxin/Pretrain-data/wulindong/sft_data/OpenOrca_format')
    args_parser.add_argument('--save_path', type=str,default='/mnt/vepfs/lingxin/Pretrain-data/wulindong/sft_data/CodeGPT/code-text_format')
    args_parser.add_argument('--pool_num', type=int,default = 12)
    # parse
    args = args_parser.parse_args()
    return args

if __name__ == '__main__':
    args = get_args()
    json_files = []
    for root, dirs, files in os.walk(args.dataset_path):
        for file in files:
            if file.endswith('.jsonl'):
                json_files.append(os.path.join(root, file))
    # result = []
    count = 0
    for path in json_files: 
        save_path = os.path.join(args.save_path,path.split('/')[-1])
        result = []
        with open(path,'r',encoding='utf-8')as file:
            # all_data = file.read().replace(r'\\n', '\\n')
            all_data = list(map(json.loads,file.readlines()))
            # all_data = json.loads(file.read())
            count+=len(all_data)
            # for line in all_data:
            #     # if line[INPUT] == '':
            #     #     input = {'input':line[INSTRUCTION]}
            #     # else:
            #     #     input = {'input':line[INSTRUCTION]+'\n'+line[INPUT]}
            #     system = {'system':line['system']}
            #     input = {'input':line['user']}
            #     output = {'output':line['assistant']}
            #     # output = {'output':line[OUTPUT]+'\n'+line['ans']}
            #     dialog = [system,input,output]
            #     result.append(json.dumps({'type':['code',{"dataset_name":"CodeGPT/code-text"}],'dialog':dialog},ensure_ascii=False))
        # if os.path.exists(args.save_path):
        #     with open(save_path,'w',encoding='utf-8')as file1:
        #         file1.write('\n'.join(result))
        # else:
        #     os.mkdir(args.save_path)
        #     with open(save_path,'w',encoding='utf-8')as file1:
        #         file1.write('\n'.join(result)) 
    
    print(count)