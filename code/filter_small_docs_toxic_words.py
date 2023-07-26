# -*- coding: UTF-8 -*-
'''
=================================================
@Author : Senbao Shi
@Date   : 2023/5/4 15:15
@Desc   : 
=================================================
'''
import argparse
import json



def get_args():
    args_parser = argparse.ArgumentParser(description='small_docs_and_toxic_words')

    args_parser.add_argument('--index', type=int)

    # parse
    args = args_parser.parse_args()

    return args



if __name__ == '__main__':
    # 1.args
    args = get_args()
    print(args)


    with open(f'/mnt/vepfs/lingxin/pretrain/wulindong/baike_2/baike_{args.index}.json', encoding="utf-8") as f:
        raw_data = [json.loads(line) for line in f]
    min_word = 32
    data_list = [data for data in raw_data if len(data['text']) >= min_word]
    print(f'raw data: {len(raw_data)} filter small docs: {len(data_list)}')
    with open(f'/mnt/vepfs/lingxin/pretrain/wulindong/baike_3/baike_{args.index}.json','w',encoding="utf-8") as f1:
        f1.writelines(json.dumps(x, ensure_ascii=False) + "\n" for x in data_list)
    print(f'/mnt/vepfs/lingxin/pretrain/wulindong/baike_3/baike_{args.index}.json  save successful')
    




    pass
