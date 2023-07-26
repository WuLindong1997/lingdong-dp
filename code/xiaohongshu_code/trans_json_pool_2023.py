import argparse
import json
import ast
import multiprocessing
import re
#2023年
from tqdm import tqdm
import os
def get_json(line):
    try:
        line = line.split('\t')[-1]
        # print(line)
        line = ast.literal_eval(line)
        line = json.loads(line['raw'], strict=False)
        liked_count = line['data'][0]['note_list'][0]['liked_count']
        collected_count = line['data'][0]['note_list'][0]['collected_count']
        title = line['data'][0]['note_list'][0]['title']
        desc = line['data'][0]['note_list'][0]['desc']
        text_dic = {}
        text  = title+'\n'+desc
        text_dic['text'] =text.strip('\n')
        text_dic['liked_count'] = liked_count
        text_dic['collected_count'] = collected_count

        json_str_cn = json.dumps(text_dic, ensure_ascii=False)
        return json_str_cn
    except:
        print('有问题')
        return None

def trans_data(path):
    
    batch_size = 400000  # 每次读取的行数
    counter = 1  # 计数器，记录已经处理的行数
   
    with open(path, "r", encoding='utf-8') as f:
        with multiprocessing.Pool(10) as pool:
            num = 1
            while True:
                batch_list = []
                flag = 1
                for i in tqdm(range(batch_size)):    
                    batch = f.readline()
                    if not batch:
                        flag = 0
                        break
                    batch_list.append(batch)
                print(f"Read {len(batch_list)} lines of data")
                results = list(tqdm(pool.imap_unordered(get_json, batch_list),total=len(batch_list)))
                
                #每batch_size行进行保存一个json文件
                root = args.save_path.split('.json')[0]
                output_path = root+f'_{counter}.json'  # 根据计数器生成输出文件名
                with open(output_path, "w", encoding='utf-8') as out_file:
                    result1 = []
                    for result in results:
                        if result is  None:
                            continue
                        result1.append(result)
                    out_file.write('\n'.join(result1))
                proce = len(result)/batch_size
                print(f'Cleaning ratio：{proce*100}%')
                counter += 1
                if flag == 0:
                    break 
    
    
   
    # with open(args.save_path, 'w', encoding='utf-8') as file:
        
    #     result1 = []
    #     for line in result:
    #         if line is not None:
    #             result1.append(line)
    #     file.write('\n'.join(result1))

def get_args():
    parser = argparse.ArgumentParser("clean xiaohongshu data")
    parser.add_argument('--data_path',type=str,default= '/mnt/vepfs/lingxin/pretrain/wulindong/code/xiaohongshu_code/note_20230407')
    parser.add_argument('--save_path',type=str,default= './note_20230407.json')
    return parser.parse_args()


if __name__ == '__main__':
    args = get_args()
    trans_data(args.data_path)
