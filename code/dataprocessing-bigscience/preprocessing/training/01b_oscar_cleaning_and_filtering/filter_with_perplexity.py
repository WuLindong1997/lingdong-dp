import os
import sys
import datasets
from multiprocessing import Pool
import json
from tqdm import tqdm
import argparse

# FILE_PATH = "/mnt/vepfs/lingxin/pretrain/wulindong/xiaohongshu_4/"
# SAVE_PATH = "/home/szt/zzh/LLM/asc/asc_ppl/asc_ppl.json"
def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset_path", type=str, default = '/pretrain-data-bucket/pretrain_other/pretrain_else/wx_temp/zh')
    parser.add_argument("--save_path", type=str,default = '/pretrain-data-bucket/pretrain_other/pretrain_else/weixin_page_dudmp_special_token_again/weixin_page.2018_special_token_3000.jsonl')
    return parser.parse_args()

def combinedata(ds,start,num):
    res = []
    for i in range(num):
        line = ds[start+i]
        res.append({'text':line['text']})
    return res

    
def save_json(res,mode='w',encoding='utf-8'):
    with open(save_path, mode=mode,encoding=encoding,) as f:
        for i in range(len(res)):       
            json.dump(res[i],f,ensure_ascii=False)
            f.write('\n')

# df = pa.ipc.open_file(file_path).read_pandas()
# print(df)
if __name__ == '__main__':
    pool = Pool(40)
    args = get_args()
    ds = datasets.load_from_disk(args.dataset_path)['train']
    save_path = args.save_path
    seg_num = 10000
    idx = 0
    max_num = ds.num_rows
    tqdm_bar = tqdm(range(1+max_num//seg_num))
    tqdm_bar.set_description("Processing")
    
    while idx < max_num:
        num = seg_num if max_num - idx >= seg_num else max_num - idx
        pool.apply_async(combinedata,args=(ds,idx,num),callback=save_json)
        tqdm_bar.update(1)
        idx += num
    pool.close()
    pool.join()
    