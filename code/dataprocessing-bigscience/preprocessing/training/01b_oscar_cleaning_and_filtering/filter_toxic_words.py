import os
import sys
import json
from tqdm import tqdm
from multiprocessing import Pool,Manager

from utils.data_util import *

manager = Manager()
stats = {'total':0,'filtered':0}
stats = manager.dict(stats)
file_path = "/home/szt/zzh/LLM/asc/asc-v1.json"
save_path = "/home/szt/zzh/LLM/asc/asc-v2.json"
toxic_path = "/home/szt/zzh/LLM/mydataprocessing/filterwords/toxic.txt"


def filter_toxic_words(data,filtered_words,key_name="text"):
    res = []
    for line in data:
        flag = True
        for item in filtered_words:
           if item in line[key_name]:
               flag = False
               break
        if flag:
            res.append(line)
    return res 
            
def save_file(res):
    stats['filtered'] += len(res)
    save_json(res,save_path,mode='a')


if __name__=='__main__':
    
    pool = Pool(32)
    
    pbar = tqdm(total=59132213)
    
    with open(toxic_path,'r',encoding='utf-8') as f:
        toxic_words = f.readlines()
    toxic_words = [i.replace('\n',"") for i in toxic_words]
    
    for data in load_json_yield(input_path=file_path):
        # print(data[0])
        pool.apply_async(func=filter_toxic_words,args=(data,toxic_words),callback=save_file)
        # res = filter_small_docs(data)
        # save_file(res)
        pbar.update(1024)
        stats['total'] += len(data)
        # stats['filtered'] += len(data)
        # filtered_num += len(data) - len(res)
        # save_json(res,output_path=save_path,mode='a')
    pool.close()
    pool.join()
    print("filtered num:{}".format(stats['filtered']))
    print("total_num:{}".format(stats['total']))