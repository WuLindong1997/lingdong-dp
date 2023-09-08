import os
import json
import re
from tqdm import tqdm

def get_data(path):
    with open(path,'r',encoding= 'utf-8')as file:
        all_data = list(map(json.loads,file.readlines()))
    all_data = [i for i in all_data if len(i['text'])>1]
    return all_data

if __name__ == "__main__":
    root_path = '/mnt/vepfs/lingxin/Pretrain-data/wulindong/markdown_process/data/clean_markdown'
    list_input_path = []
    for path in os.listdir(root_path):
        list_input_path.append(os.path.join(root_path,path))

    result = []
    for input_path in tqdm(list_input_path,total=len(list_input_path)):
        data = get_data(input_path)
        result.extend(data)
    start = len(result)//2
    result1 = result[:start-10000]
    result2 = result[start-10000:]
    with open('/mnt/vepfs/lingxin/Pretrain-data/wulindong/markdown_process/data/markdown_train.jsonl','w',encoding="utf-8")as file:
        for i in result1:
            file.write(json.dumps(i,ensure_ascii=False))
            file.write('\n')
        
    with open('/mnt/vepfs/lingxin/Pretrain-data/wulindong/markdown_process/data/markdown_no_train.jsonl','w',encoding="utf-8")as file1:
        for i in result2:
            file1.write(json.dumps(i,ensure_ascii=False))        
            file1.write('\n')