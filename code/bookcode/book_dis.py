import os
import argparse
import json
def get_args():
    args_parser = argparse.ArgumentParser()
    # dictionary or file
    args_parser.add_argument('--dataset_path', type=str,default='/mnt/vepfs/lingxin/Pretrain-data/wulindong/code/bookcode/bookdata_clean_end')
    args_parser.add_argument('--save_path', type=str,default='/mnt/vepfs/lingxin/Pretrain-data/wulindong/code/bookcode/length.json')
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
    len_dict = {}
    for path in json_files:
        with open(path,'r',encoding='utf-8')as file2:
            all_data = file2.readlines()
        json_data = list(map(json.loads,all_data))

        for line in json_data:
            text = line['text']
            length = len(text)
            if str(length) in list(len_dict.keys()):
                len_dict[str(length)]+=1
            else:
                len_dict[str(length)] = 1
    with open(args.save_path,'w',encoding='utf-8')as file1:
        file1.write(json.dumps(len_dict,ensure_ascii=False))