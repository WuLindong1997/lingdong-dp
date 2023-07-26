import argparse
from bs4 import BeautifulSoup
import json
import re
from tqdm import tqdm
import multiprocessing
import os
import random
import io
def process_json(data):

    text_json = json.loads(data)
    text = text_json['text']
    #这里切分之后，判断切分后有多少段，暂定超过10段的删除最后2段。
    text_list = text.split('\n')
    if len(text_list)>=10:
        text_list = text_list[:-2]
    

    #切分去除包含关键字的段落
    text1 = ''
    for line in text_list:
        flage = 1
        for keyword in ['原创','咨询','原作者','微信群','https','http','www','二维码','公众号','会员专属','培训费','普通会员','高级会员','VIP 会员','QQ论坛','精彩马上开始','首播时间','往期回顾','点关注','搜索号码','版权归','分享到朋友圈','每日更新','V信','关注我们','点击下方关注','识别下方二维码','转发到','注：本文转载','注：本文','编辑：', '监制：', '电话：', '邮箱：', '主办：', '来源：',
            '留言','iOS','下方','来源','版权','侵权','审核：', '校审：', '校对：', '编审：', '摄像：', '责编：', '策划：', '排版：', '初审：','微信：','扩展阅读','关注',
            '编辑 ', '监制 ', '电话 ', '邮箱 ', '主办 ', '来源 ','微信号','加客服好友','商务合作','复审 ','终审 ',
            '审核 ', '校审 ', '校对 ', '编审 ', '摄像 ', '责编 ', '策划 ', '排版 ', '初审 ','长按识别下方','长按识别二维码',
            '编辑｜','点“阅读原文”','免责声明','请点阅读原文','微信','电话','侵犯版权','记者','咨询人数','扫码','粉丝群']:
            if keyword in line:
                flage = 0
                break
        if flage==1:
            text1+=line+'\n'
    text = text1.strip('\n')
    text = re.sub(r'\s{2,}', ' ', text)
    dict_text = {}
    dict_text['text']= text
    json_text = json.dumps(dict_text,ensure_ascii=False)
    return json_text

    


       

def get_args():
    args_parser = argparse.ArgumentParser(description='parse_html')

    # dictionary or file
    args_parser.add_argument('--dataset_path', type=str,default='/pretrain-data-bucket/pretrain_other/pretrain_else/xiaohongshu_save_emoji_end')
    args_parser.add_argument('--save_path', type=str,default='/mnt/lingxin/vepfs/pretrain/wulindong/xiaohongshu.json')
    args_parser.add_argument('--pool_num', type=int,default = 12)

    # parse
    args = args_parser.parse_args()

    return args



if __name__ == '__main__':
    # 1.args
    args = get_args()
    data_dir = '/pretrain-data-bucket/pretrain_other/pretrain_else/xiaohongshu_save_emoji_end'
    json_files = []
    for root, dirs, files in os.walk(data_dir):
        for file in files:
            if file.endswith('.json'):
                json_files.append(os.path.join(root, file))
    result = []
    for path in tqdm(json_files):
        try:
            with open(path,'r',encoding='utf-8')as file:
                all_data = file.read().split('\n')[:-1]
            length = len(all_data)
            get_data = [all_data[random.randint(0,length)] for i in range(2)]
            for line in get_data:
                
                result.append(line)
        
        except:
            pass
    with open('/mnt/vepfs/lingxin/pretrain/wulindong/weixin_sample.json','w',encoding='utf-8')as file1:
        data = '\n'.join(result)
        file1.write(data)
