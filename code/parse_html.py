# -*- coding: UTF-8 -*-
'''
=================================================
@Author : Senbao Shi
@Date   : 2023/5/7 23:48
@Desc   : 
=================================================
'''
import argparse
from bs4 import BeautifulSoup
import json
import re
from tqdm import tqdm
import time
def paser_text(content):

    html_content = content

    # Parse the HTML content with BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    #首先提取内容部分
    soup = soup.find('div',attrs={'class':'content'})

    # 删除表格
    for table in soup.find_all('table'):
        # td.string = ''
        table.decompose()

    # 删除所有图片下面的文字
    # 删除所有 class 为 'description' 的 span 标签
    for span in soup.find_all('span', {'class': 'description'}):
        span.decompose()

    # 清空 span 标签中的内容 标题会反复出现在span标签中
    for span in soup.find_all('span', {'class': 'title-prefix'}):
        # span.string = ''
        span.decompose()

    # 清空 span 标签中的内容 编辑、播报
    for span in soup.find_all('span', {'class': 'J-part-audio-text'}):
        # span.string = ''
        span.decompose()
    for a in soup.find_all('a', {'class': 'edit-icon j-edit-link'}):
        # a.string = ''
        a.decompose()

    # # Find the HTML elements that contain the text you want to extract
    # intros = soup.find_all('div', {'class': 'para'})
    intros = soup.find_all(['div', 'h2', 'h3'], {'class': ['para-title', 'para']})
    # intros_parent_empty = [intros[i] for i in range(len(intros))
    #                        if i < len(intros) - 1 and intros[i] in intros[i-1].parents and len(intros[i].get_text().strip()) == 0]
    # intros = soup.find_all(['h1', 'h2', 'h3', 'div', 'p'])
    # intros = [intro.get_text().strip() for intro in intros if len(intro.get_text().strip()) > 0]
    intros = [intro.text.strip() for intro in intros if len(intro.get_text().strip()) > 0]
    intros = [intro.replace('\n', '').replace('\xa0', '').strip() for intro in intros] # 去掉间隔符号
    intros = [re.sub(r'\[\d+(?:-\d+)?\]', '', intro) for intro in intros] # 去掉引用符号

    # Extract the text from the HTML elements
    text = ''
    for elem in intros:
        text += elem + '\n'

    # print(text)
    # Print the extracted text
    return text


def get_args():
    args_parser = argparse.ArgumentParser(description='parse_html')

    # dictionary or file
    args_parser.add_argument('--index', type=int,default=2000)

    # parse
    args = args_parser.parse_args()

    return args


if __name__ == '__main__':
    # 1.args
    args = get_args()
    print(args)
    start_time = time.time()
    data_list = []
    with open(f'/mnt/vepfs/lingxin/pretrain/wulindong/baike/baike_{args.index}.txt', "r", encoding='utf-8') as f:
        data = f.readlines()  # 读取文本
        for d in tqdm(data):
            tmp_dict = json.loads(d)
            content = tmp_dict['content']
            text = paser_text(content)
            data_list.append({'text': text})
    # save as json file
    with open(f'/mnt/vepfs/lingxin/pretrain/wulindong/baike_1/baike_{args.index}.json', 'w', encoding='utf-8') as f:
        f.writelines(json.dumps(x, ensure_ascii=False) + "\n" for x in data_list)
    end_time = time.time()
    total_time = end_time - start_time
    print(f"程序执行时间：{total_time:.2f}秒")
    pass
