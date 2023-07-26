import os
import sys
import datasets
from multiprocessing import Pool
import json
from tqdm import tqdm
import argparse

# FILE_PATH = "/home/szt/zzh/LLM/asc/asc_ppl/zh/train"
# SAVE_PATH = "/home/szt/zzh/LLM/asc/asc_ppl/asc_ppl.json"
def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset_path", type=str, default = '/mnt/vepfs/lingxin/pretrain/wulindong/xiaohongshu_3/note_20230309.json')
    parser.add_argument("--save_path", type=str,default = '/mnt/vepfs/lingxin/pretrain/wulindong/xiaohongshu_4/note_20230309.json')
    return parser.parse_args()
def combinedata(ds,start,num):
    res = []
    for i in range(num):
        line = ds[start+i]
        res.append({'text':line['text']})
    return res

    
def save_json(res,mode='a',encoding='utf-8'):
    args = get_args()
    with open(args.save_path, mode=mode,encoding=encoding,) as f:
        for i in range(len(res)):       
            json.dump(res[i],f,ensure_ascii=False)
            f.write('\n')

# df = pa.ipc.open_file(file_path).read_pandas()
# print(df)
if __name__ == '__main__':
    pool = Pool(8)
    args = get_args()
    # ds = datasets.load_from_disk(args.dataset_path)
    ds = datasets.load_dataset("json", data_files=args.dataset_path)['train']
    
    seg_num = 1000
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