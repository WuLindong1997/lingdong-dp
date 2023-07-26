import os
import json
import re
from tqdm import tqdm
import multiprocessing



def process_data(list_path):
    
    for path in tqdm(list_path):
        with open(path,'r',encoding='utf-8') as file:
            list_text = [json.loads(line)['text'] for line in file.read().split('\n')]
            for line in list_text:
                list_class = re.findall(r'#.*?#',line)
                if list_class is not None:
                    for i in list_class:
                        if i in class_dict.keys():
                            class_dict[i]+= 1
                        else:
                            class_dict[i] = 1 

if __name__ =='__main__':
    root_path = '/pretrain-data-bucket/pretrain_other/pretrain_else/xiaohongshu_save_emoji_end'
    list_name = os.listdir(root_path)
    list_path = [os.path.join(root_path, file_name) for file_name in list_name]
    class_dict={}
    process_data(list_path)
    
    
    with open('/mnt/vepfs/lingxin/pretrain/wulindong/xiaohongshu_classes.json','w',encoding='utf-8') as file1:
        file1.write(json.dumps(class_dict, ensure_ascii=False))