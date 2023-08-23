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
    # text = emoji_regex.sub(r"", text)
    for word in toxic_words:
        if word in text:
            return None
    if len(text)<80:
        return None
    json_text = json.dumps(text_json,ensure_ascii=False)
    return json_text

    


       

def get_args():
    args_parser = argparse.ArgumentParser(description='parse_html')

    # dictionary or file
    args_parser.add_argument('--dataset_path', type=str,default='/pretrain-data-bucket/pretrain_other/pretrain_else/weixin_page_end_again')
    # args_parser.add_argument('--dataset_path', type=str,default='/pretrain-data-bucket/pretrain_other/pretrain_else/weixin_page_clean_special_token/')
    args_parser.add_argument('--save_path', type=str,default='/pretrain-data-bucket/pretrain_other/pretrain_else/weixin_page_end')
    args_parser.add_argument('--pool_num', type=int,default = 8)

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
    with open('/mnt/vepfs/lingxin/pretrain/wulindong/weixin_page/code/clean_weixin/toxic.txt','r',encoding='utf-8') as f:
        toxic_words = f.readlines()
    toxic_words = [i.replace('\n',"") for i in toxic_words]
    save_path_root = args.save_path
    for path in json_files:
        filename0 = path.split('/')[-1]
        filename1 = path.split('/')[-2]
        if os.path.exists(os.path.join(save_path_root,filename1,filename0)):
            print(f'{os.path.join(save_path_root,filename1,filename0)} skip!')
            continue
        with multiprocessing.Pool(args.pool_num) as pool:
            try:

                with open(path,'r',encoding='utf-8')as file:
                    all_data = file.read().split('\n')[:-1]
                process_data_partial = partial(process_json, toxic_words=toxic_words)
                results = list(tqdm(pool.map(process_data_partial, all_data),total=len(all_data)))
                filtered_results = [r for r in results if r is not None]
                print(f'clean roit:{len(filtered_results)/len(all_data)*100}%')
                d_file_name = path.split('/')[-2]
                name = path.split('/')[-1]
                directory = os.path.join(save_path_root,d_file_name)
                if not os.path.exists(directory):
                    os.mkdir(directory)
                    print("目录 '%s' 创建成功！" % directory)
                save_name = os.path.join(directory,name)
                with open(save_name,'w',encoding='utf-8')as file1:
                    file1.write('\n'.join(filtered_results))
            except:
                print(f"{path} 存在问题")
    
