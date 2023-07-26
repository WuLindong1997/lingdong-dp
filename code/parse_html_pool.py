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
import multiprocessing
def paser_text(content):
    html_content = content

    # Parse the HTML content with BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')
    # 去除表格上面横线的div
    lines = soup.find_all('div', attrs={'class': 'anchor-list'})
    for line in lines:
        line.extract()

    # 查找div class=starMovieAndTvplay，删除并查找上面的兄弟是否为div class = para-title level-2 J-chapter
    movies = soup.find_all('div', attrs={'class': 'starMovieAndTvplay'})
    for movie in movies:
        try:
            prev_movie = movie.find_previous_sibling()
            if prev_movie.name == 'div' and ' '.join(prev_movie.get('class')) == 'para-title level-3 MARK_MODULE':
                prev_movie.extract()
        except:
            pass
    # 查找所有表格，如果表格上方为div class = para-title level-2 J-chapter
    tables = soup.find_all('table')
    for table in tables:
        try:
            # 找到表格的上一个兄弟元素
            prev_sibling = table.find_previous_sibling()
            # 在上一个兄弟元素中查找符合条件的元素
            if prev_sibling.name == 'div' and ' '.join(prev_sibling.get('class')) == 'para-title level-2 J-chapter':
                prev_sibling.extract()
        except:
            pass
        # 删除表格
        table.extract()

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

    intros = [intro.replace('\n', '').replace('\xa0', '').strip() for intro in intros]  # 去掉间隔符号
    intros = [re.sub(r'\[\d+(?:-\d+)?\]', '', intro) for intro in intros]  # 去掉引用符号

    # Extract the text from the HTML elements
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
    return text


def get_args():
    args_parser = argparse.ArgumentParser(description='parse_html')

    # dictionary or file
    args_parser.add_argument('--index', type=int)
    args_parser.add_argument('--pool_num', type=int,default = 24)

    # parse
    args = args_parser.parse_args()

    return args

def process_data(d):
    tmp_dict = json.loads(d)
    content = tmp_dict['content']
    text = paser_text(content)
    return {'text': text}

if __name__ == '__main__':
    # 1.args
    args = get_args()

    print(args)

    data_list = []
    #with open(f'/mnt/vepfs/lingxin/pretrain/shisenbao/move1/baike_{args.index}.txt', "r", encoding='utf-8') as f:
    with open(f'/mnt/vepfs/lingxin/pretrain/wulindong/baike/baike_{args.index}.txt', "r", encoding='utf-8') as f:
        data = f.readlines()  # 读取文本
        with multiprocessing.Pool(args.pool_num) as pool:
            data_list = list(tqdm(pool.imap(process_data, data), total=len(data)))

    # save as json file
    with open(f'/mnt/vepfs/lingxin/pretrain/wulindong/baike_1/baike_{args.index}.json', 'w', encoding='utf-8') as f:
        f.writelines(json.dumps(x, ensure_ascii=False) + "\n" for x in data_list)

    pass
