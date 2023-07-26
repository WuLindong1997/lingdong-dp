import argparse
from bs4 import BeautifulSoup
import json
import re
from tqdm import tqdm
import multiprocessing
import os
def paser_text(content):
    html_content = content
    try:

        # Parse the HTML content with BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')

        # 首先缩小范围：
        soup = soup.find('div', class_="rich_media_wrp")
        #————————————这里填写去除有毒标签的规则——————————————
        # image去除
        images = soup.find_all('image')
        for image in images:
            image.extract()
        # 去除表格
        tables = soup.find_all('table')
        for table in tables:
            table.extract()
        #—————————————这里填写去除有毒标签的规则——————————————
        intros = soup.find_all(['h1', 'h2','h3','h4','p'])
        
        intros = [intro.text.strip() for intro in intros if len(intro.get_text().strip()) > 0]

        # intros = [intro.replace('\n', '').replace('\xa0', '').strip() for intro in intros]  # 去掉间隔符号
        intros = [re.sub(r'\[\d+(?:-\d+)?\]', '', intro) for intro in intros]  # 去掉引用符号


        text = ''
        text_list = []
        if len(intros) > 0:
            count = 0
            for index in range(len(intros)):
                if intros[index] != '':
                    text_list.append(intros[index])
                else:
                    if len(text_list) > 0:
                        text_list.pop()

        text = '\n'.join(text_list)
        # print(text)
        # Print the extracted text
        #——————————————这里添加正则————————————————
        pattern = r'微信号\n[a-z].*?\n'
        text = re.sub(pattern, '', text)
        pattern = r'微信号.*?\n'
        text = re.sub(pattern, '', text)
        pattern = r'（.*?）'
        text = re.sub(pattern, '', text)
        pattern = r'\n[a-zA-Z0-9-]+\n'
        text = re.sub(pattern, '', text)
        text = text.replace('功能介绍','')
        pattern = r'[\n,.。，\n\t].*?电话.*?[0-9｜、]+'
        text = re.sub(pattern,'',text)
        #只保留中文和英文字符和标点符号
        text = re.sub(r'[^\u4e00-\u9fa5a-zA-Z0-9，。！？、；：“”‘’（）《》\s]', '', text)

        #去除http链接
        url_pattern = re.compile(r'(http|https|www):[^\u4e00-\u9fff]+')
        text =  url_pattern.sub('', text)
        #切分然后，查看切分中是否包含关键字
        text_list1 = text.split('\n')
        text1 = ''
        for line in text_list1:
            flage = 1
            for keyword in ['精彩马上开始','首播时间','往期回顾','点关注','搜索号码','版权归','分享到朋友圈','每日更新','V信','关注我们','点击下方关注','识别下方二维码','转发到','注：本文转载','注：本文','编辑：', '监制：', '电话：', '邮箱：', '主办：', '来源：',
                '审核：', '校审：', '校对：', '编审：', '摄像：', '责编：', '策划：', '排版：', '初审：','微信：','扩展阅读',
                '编辑 ', '监制 ', '电话 ', '邮箱 ', '主办 ', '来源 ','微信号','加客服好友','商务合作','复审 ','终审 ',
                '审核 ', '校审 ', '校对 ', '编审 ', '摄像 ', '责编 ', '策划 ', '排版 ', '初审 ','长按识别下方','长按识别二维码',
                '编辑｜','点“阅读原文”','免责声明','请点阅读原文','微信','电话','侵犯版权','记者','咨询人数','扫码','粉丝群']:
                if keyword in line:
                    flage = 0
                    break
            if flage==1:
                text1+=line+'\n'
        text = text1.strip('\n')
        text_list2 = text.split('\n')
        text1 = ''
        for line in text_list2:
            if re.search(r'[,，。‘’“”；！？?!.:;]', line):
                text1+=line+'\n'

        text = text1.strip('\n')
        
        #替换2个以上个相同的标点符号，变成一个
        pattern = r'([^\w\s])\1{2,}'
        text = re.sub(pattern, r'\1\1', text)
        text = text.replace('\n\n','\n')
        # 去除一些特殊符号
        special = ['►', '▼', '▶','✅','◆', '③','㊙','\u00a0', '\u3000','-']
        for sp in special:
            text = text.replace(sp, '')
        emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               "]+", flags=re.UNICODE)
        text = emoji_pattern.sub(r'', text)
        

        #——————————————这里添加正则————————————————
        return text
    except:
        print("找不到标签，返回空！")
        return ''


def get_args():
    args_parser = argparse.ArgumentParser(description='parse_html')

    # dictionary or file
    args_parser.add_argument('--dataset_path', type=str,default='/pretrain-data-bucket/pretrain_other/pretrain_else/weixin_page.2022-01-01')
    args_parser.add_argument('--save_path', type=str,default='/mnt/vepfs/lingxin/pretrain/wulindong/')
    args_parser.add_argument('--pool_num', type=int,default = 10)
    args_parser.add_argument('--batch_size', type=int,default = 60000)


    # parse
    args = args_parser.parse_args()

    return args

def process_data(d):
    d = d.split('\t', maxsplit=1)[1].strip('\n')
    tmp_dict = json.loads(d) 
    content = tmp_dict['content']
    text = paser_text(content)
    text = json.dumps({'text': text},ensure_ascii=False)
    return text

if __name__ == '__main__':
    # 1.args
    args = get_args()
    
    
    batch_size = args.batch_size  # 每次读取的行数
    counter = 1  # 计数器，记录已经处理的行数
    file_name = args.dataset_path.split('/')[-1]
    with open(args.dataset_path, "r", encoding='utf-8') as f:
        with multiprocessing.Pool(args.pool_num) as pool:
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
                results = list(tqdm(pool.imap_unordered(process_data, batch_list),total=len(batch_list)))
                
                #每batch_size行进行保存一个json文件

                output_path = os.path.join(args.save_path,f'{file_name}_{counter}.json')  # 根据计数器生成输出文件名
                with open(output_path, "w", encoding='utf-8') as out_file:
                    for result in results:
                        if len(json.loads(result)['text'])<50:
                            continue
                        out_file.write(result + '\n')
                proce = len(result)/batch_size
                print(f'Cleaning ratio：{proce*100}%')
                counter += 1
                if flag == 0:
                    break
            
 
