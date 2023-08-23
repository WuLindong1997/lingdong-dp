import argparse
from bs4 import BeautifulSoup
import json
import re
from tqdm import tqdm
import multiprocessing
import os
import io
from functools import partial
def process_json(data,toxic_words):

    text_json = json.loads(data)
    text = text_json['text']
    # text = re.sub(r'\s{2,}', ' ', text)                                                                                                                                     
    # text = emoji_regex.sub(r"", text)
    
    #这里切分之后，判断切分后有多少段，暂定超过10段的删除最后2段。
    text_list = text.split('\n')
    
    #切分去除包含关键字的段落
    text1 = ''
    for line in text_list:
        flage = 1
        for keyword in toxic_words:
            if keyword in line:
                flage = 0
                break
        if flage==1:
            text1+=line+'\n'
    text = text1.strip('\n')
    

    if len(text) < 110 :
        return 
    dict_text = {}
    dict_text['text']= text
    json_text = json.dumps(dict_text,ensure_ascii=False)
    return json_text

    


       

def get_args():
    args_parser = argparse.ArgumentParser(description='parse_html')

    # dictionary or file
    args_parser.add_argument('--dataset_path', type=str,default='/pretrain-data-bucket/pretrain_other/pretrain_else/weixin_page_dudmp_special_token')
    # args_parser.add_argument('--dataset_path', type=str,default='/pretrain-data-bucket/pretrain_other/pretrain_else/weixin_page_clean_special_token/')
    args_parser.add_argument('--save_path', type=str,default='/pretrain-data-bucket/pretrain_other/pretrain_else/weixin_temp')
    args_parser.add_argument('--pool_num', type=int,default = 30)

    # parse
    args = args_parser.parse_args()

    return args



if __name__ == '__main__':
    # 1.args
    args = get_args()
    data_dir = args.dataset_path
    json_files = []
    for root, dirs, files in os.walk(data_dir):
        for file in files:
            if file.endswith('.json'):
                json_files.append(os.path.join(root, file))
    with open('/mnt/vepfs/lingxin/Pretrain-data/wulindong/weixin_page/code/clean_weixin/keyword.txt','r',encoding='utf-8') as f:
        toxic_words = f.readlines()
    toxic_words = [i.replace('\n',"") for i in toxic_words]
    save_path_root = args.save_path
    for path in json_files:
        save_path = os.path.join(save_path_root,path.split('/')[-1]) 
        with multiprocessing.Pool(args.pool_num) as pool:
            with open(path,'r',encoding='utf-8')as file:
                all_data = file.read().split('\n')[:-1]
            process_data_partial = partial(process_json, toxic_words=toxic_words)
            results = list(tqdm(pool.imap(process_data_partial, all_data),total=len(all_data)))
            filtered_results = [r for r in results if r is not None]
            
            with open(save_path,'w',encoding='utf-8')as file1:

                file1.write('\n'.join(filtered_results))
        
    
