import argparse
from bs4 import BeautifulSoup
import json
import re
from tqdm import tqdm
import multiprocessing
import os
import io
import emoji

SPECIAL_TAG_FORMAT = {
    "code_block": ("[CODE_START]\n"
                   "```\n"
                   "{code_string}"
                   "```\n"
                   "[CODE_END]"),
    "code_inline": " `{code_string}` ",
    "formula_block": "[EQ_START]\n{formula_string}\n[EQ_END]",
    "formula_inline": " $ {formula_string} $ ",
    "img": "[IMG_START] {img_src} [IMG_END]",
    "table": "[TAB_START] {table_string} [TAB_END]",
    "emoji": "[EMJ_START] {emoji_string} [EMJ_END]",
}


def chinese_ratio(text):
    if len(text) == 0:
        return 0
    chinese_chars = re.findall(r'[\u4e00-\u9fff]', text)
    return len(chinese_chars) / len(text)


def line_filter(line):
    if len(line) < 1:
        return False
    elif line.count("=") / len(line) > 0.7:
        return False
    else:
        return True


def clean_string(line):
    # replace white space
    return line.replace("\u3000", " ").replace("\u200b", " ").replace("u3000", " ").replace("u200b", " ").replace("﻿",
                                                                                                                  " ").replace(
        "↓", " ")


def add_hashtags_to_emoji(text):
    def replace_emoji(match):
        return SPECIAL_TAG_FORMAT["emoji"].format(emoji_string=match.group(0))

    pattern = emoji.get_emoji_regexp()
    return re.sub(pattern, replace_emoji, text)


def paser_text(content):
    html_content = content
    try:
        # with open('/mnt/vepfs/lingxin/pretrain/wulindong/weixin_page/code/clean_weixin/a.html','r',encoding='utf-8') as file1:
        #     html_content = file1.read()
        # Parse the HTML content with BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')
        # 首先缩小范围：
        soup = soup.find('div', class_="rich_media")
        soup_results = soup.find_all(['h1', 'h2', 'h3', 'h4', 'p', 'img', 'table', 'span', 'pre'])
        page_text = ''
        for result in soup_results:
            if result.name == "table":
                # Table
                table_text = '\n'.join([str(c) for c in result.contents])
                table_text = clean_string(table_text)
                return SPECIAL_TAG_FORMAT["table"].format(table_string=table_text) + '\n'

            elif result.name == "img" and result.get("src") and len(result["src"].strip()) > 0:
                if result.get("alt"):
                    # formula
                    formula_text = result["alt"].strip()
                    if formula_text.endswith("\\\\"):
                        line_text = SPECIAL_TAG_FORMAT["formula_block"].format(formula_string=formula_text)
                        page_text = page_text + clean_string(line_text) + "\n"
                    else:
                        line_text = SPECIAL_TAG_FORMAT["formula_inline"].format(formula_string=formula_text)
                        page_text = page_text.strip() + clean_string(line_text)
                else:
                    # imgage hyperlink
                    line_text = SPECIAL_TAG_FORMAT["img"].format(img_src=result["src"].strip())
                    page_text = page_text + clean_string(line_text) + "\n"
            elif result.name == "span":
                # in segment
                if result.get('data-formula') and result.get('data-formula-type')[0] == 'inline-equation':
                    eq_text = result.text.strip()
                    line_text = SPECIAL_TAG_FORMAT['formula_block'].format(formula_string=eq_text)
                    page_text = page_text + clean_string(line_text)
                # on segment
                elif result.get('data-formula') and result.get('data-formula-type')[0] == 'block-equation':
                    eq_text = result.text.strip()
                    line_text = SPECIAL_TAG_FORMAT['formula_block'].format(formula_string=eq_text)
                    page_text = page_text + clean_string(line_text) + '\n'

            elif result.name == "pre" and result.find_all('code'):
                # Code: Code block or inlince code
                codes = result.find_all('code')
                code_text = ''
                if codes != []:
                    for code in codes:
                        code_text = code_text + code.text + '\n'

                    # TODO: inline code shouldn't append '\n'
                line_text = SPECIAL_TAG_FORMAT["code_block"].format(code_string=code_text)
                page_text = page_text.strip() + clean_string(line_text)


            else:
                line_text = clean_string(result.text.strip())
                if line_filter(line_text):
                    page_text = page_text + line_text + "\n"
        page_text = page_text.replace('\n功能介绍', '')
        pattern = r'微信号\n[a-z0-9A-Z].*?\n'
        page_text = re.sub(pattern, '', page_text)
        pattern = r'微信号.*?\n'
        page_text = re.sub(pattern, '', page_text)
        page_text = add_hashtags_to_emoji(page_text)

        return page_text.strip()


    except:
        print("找不到标签，返回空！")
        return ''


def get_args():
    args_parser = argparse.ArgumentParser(description='parse_html')

    # dictionary or file
    args_parser.add_argument('--dataset_path', type=str,
                             default='/mnt/vepfs/lingxin/pretrain/wulindong/weixin_page/code/clean_weixin/weixin_page.2018-09-02')
    args_parser.add_argument('--save_path', type=str, default='/mnt/vepfs/lingxin/pretrain/wulindong/')
    args_parser.add_argument('--pool_num', type=int, default=1)
    args_parser.add_argument('--batch_size', type=int, default=600000)
    # parse
    args = args_parser.parse_args()

    return args


def process_data(d):
    text = paser_text(d)
    text = json.dumps({'text': text}, ensure_ascii=False)
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
                pages = re.findall(r"<html>.*?</html>", ''.join(batch_list), re.DOTALL)
                print(f"Read {len(pages)} lines of data")
                results = list(tqdm(pool.map(process_data, pages), total=len(pages)))

                # 每batch_size行进行保存一个json文件

                output_path = os.path.join(args.save_path, f'{file_name}_{counter}.json')  # 根据计数器生成输出文件名
                with open(output_path, "w", encoding='utf-8') as out_file:
                    for result in results:
                        if len(json.loads(result)['text']) < 50:
                            continue
                        out_file.write(result + '\n')
                proce = len(result) / batch_size
                print(f'Cleaning ratio：{proce * 100}%')
                counter += 1
                if flag == 0:
                    break