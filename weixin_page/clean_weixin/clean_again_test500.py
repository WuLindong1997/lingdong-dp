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
    # if len(text_list)>=7:
    #     text_list = text_list[:-1]
    # elif len(text_list)>=12:
    #     text_list = text_list[:-2]

    #切分去除包含关键字的段落
    text1 = ''
    for line in text_list:
        if '推荐:' in line or '推荐：' in line or '阅读更多' in line or '阅读原文' in line:
            break
        if len(re.findall(r'[a-zA-Z0-9]{46,}', line))>0:#连续不间断出现大于46个数字或英文字符（最长的英文单词长45）
            break
        flage = 1
        if len(line) == 1:
            continue
        for keyword in toxic_words:
            if keyword in line:
                flage = 0
                break
        if flage==1:
            text1+=line+'\n'
    text = text1.strip('\n')
    # text = re.sub(r'\s{2,}', ' ', text)
    # text = re.sub(r'\d{11,}', '', text)
    
    SPECIAL_TAG_FORMAT = {
        "code_block": r"\[CODE_START\](.*?)\[CODE_END\]",
        "code_inline": r"\[CODE_IN_START\](.*?)\[CODE_IN_END\]",
        "formula_block": r"\[EQ_START\](.*?)\[EQ_END\]",
        "formula_inline": r"\[EQ_IN_START\](.*?)\[EQ_IN_END\]",
        "img": r"\[IMG_START\](.*?)\[IMG_END\]",
        "table": r"\[TAB_START\](.*?)\[TAB_END\]",
        "emoji": r"\[EMJ_START\](.*?)\[EMJ_END\]",
    }
    patterns = [v for k, v in SPECIAL_TAG_FORMAT.items()]
    pattern = "|".join(patterns)
    
    text_temp = re.sub(pattern, "", text.replace("\n", "n"))
    # text_temp = re.sub(pattern, "", text)
    
    # Extract Chinese characters and English words
    chinese_chars = float(len(''.join(re.findall(r'[\u4e00-\u9fff]+', text_temp))))
    english_words = float(len(re.findall(r'\b[A-Za-z]+\b', text_temp)))

    # Compute ratios
    total_chars = chinese_chars+english_words

    if total_chars < 500:
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
    args_parser.add_argument('--save_path', type=str,default='/pretrain-data-bucket/pretrain_other/pretrain_else/weixin_page_dudmp_special_token_again_test500')
    args_parser.add_argument('--pool_num', type=int,default = 50)

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
            if file.endswith('.jsonl'):
                json_files.append(os.path.join(root, file))
    with open('/mnt/vepfs/lingxin/Pretrain-data/wulindong/weixin_page/code/clean_weixin/keyword.txt','r',encoding='utf-8') as f:
        toxic_words = f.readlines()
    toxic_words = [i.replace('\n',"") for i in toxic_words]
    save_path_root = args.save_path
    for path in json_files:
        filename0 = path.split('/')[-1]
        save_path = os.path.join(args.save_path,filename0)
        if os.path.exists(save_path):
            print(f'{save_path} skip!')
            continue
        with multiprocessing.Pool(args.pool_num) as pool:
            try:

                with open(path,'r',encoding='utf-8')as file:
                    all_data = file.read().split('\n')[:-1]
                process_data_partial = partial(process_json, toxic_words=toxic_words)
                results = list(tqdm(pool.imap(process_data_partial, all_data),total=len(all_data)))
                filtered_results = [r for r in results if r is not None]
                
                print(f"保存的位置：{save_path}")

                with open(save_path,'w',encoding='utf-8')as file1:

                    file1.write('\n'.join(filtered_results))
                    print(f"保存完成：{save_path}")
                
            except:
                print(f"{path} 存在问题")
    
