# -*- coding: UTF-8 -*-
'''
=================================================
@Author : Senbao Shi
@Date   : 2023/5/5 13:32
@Desc   : 
=================================================
'''


import requests
from bs4 import BeautifulSoup
import json
import re
from tqdm import tqdm
import os
import gzip
import shutil

def paser_text(content):

    html_content = content

    # Parse the HTML content with BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    #首先提取内容部分
    soup = soup.find('div',attrs={'class':'content'})

    # 删除表格中的文字
    for td in soup.find_all('td'):
        td.string = ''

    # 删除所有图片下面的文字
    # 删除所有 class 为 'description' 的 span 标签
    for span in soup.find_all('span', {'class': 'description'}):
        span.decompose()

    # 清空 span 标签中的内容 标题会反复出现在span标签中
    for span in soup.find_all('span', {'class': 'title-prefix'}):
        span.string = ''

    # 清空 span 标签中的内容 编辑、播报
    for span in soup.find_all('span', {'class': 'J-part-audio-text'}):
        span.string = ''
    for span in soup.find_all('a', {'class': 'edit-icon j-edit-link'}):
        span.string = ''


    # # Find the HTML elements that contain the text you want to extract
    # intros = soup.find_all('div', {'class': 'para'})
    intros = soup.find_all(['div', 'h2', 'h3'], {'class': ['para-title', 'para']})
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



if __name__ == '__main__':

    # data_list = []
    # with open('/mnt/vepfs/lingxin/pretrain/wulindong/baike/baike_2000.txt', "r", encoding='utf-8') as f:
    #     data = f.readlines()  # 读取文本
    #     for d in tqdm(data):
    #         tmp_dict = json.loads(d)
    #         content = tmp_dict['content']
    #         text = paser_text(content)
    #         data_list.append({'text': text})
    with open('/mnt/vepfs/lingxin/pretrain/wulindong/code/html2.txt','r',encoding='utf-8')as file:
        text = file.read()
    text = paser_text(text)
    data_list.append({'text': text})
    # save as json file
    with open('/mnt/vepfs/pretrain/shisenbao/raw/raw_baike_0.json', 'w', encoding='utf-8') as f:
        f.writelines(json.dumps(x, ensure_ascii=False) + "\n" for x in data_list)
    pass
