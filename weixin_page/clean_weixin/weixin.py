import json
import re

from bs4 import BeautifulSoup


def remove_html(s):
    soup = BeautifulSoup(s, 'html.parser')
    images = soup.find_all("img")
    img_num = len(images)
    s = ''
    for p in soup.find_all('p'):
        s += p.text.strip() + '\n'
    return s.strip(), img_num


def remove_last(s, suf):
    idx = s.rfind(suf)
    if idx != -1:
        s = s[:idx] + s[idx+len(suf):]
    return s.strip()


suffix = [
    '\n微信扫一扫关注该公众号',
    '\n发送中',
    '\n已发送',
    '\n前往“发现”-“看一看”浏览“朋友在看”',
    '\n留言'
]


def remove_suffix(s):
    for suf in suffix:
        s = remove_last(s, suf)
    return s


special = ['►', '▶']


def remove_special(s):
    # 去除一些特殊符号，暂时只找到'►', '▶'
    for sp in special:
        s = s.replace(sp, '')
    return s.strip()


def clean(raw_html):
    text, img_num = remove_html(raw_html)
    text = remove_suffix(text)
    text = remove_special(text)
    return text, img_num


if __name__ == '__main__':
    count = 0
    with open('weixin_page.2020-01-25.03') as f1:
        with open('tmp.json', 'w') as f2:
            line = f1.readline()
            while line:
                idx = line.find('{')
                line = line[idx:]
                json_obj = json.loads(line)
                content, image_count = clean(
                    json_obj['uncompress(content)'])
                # if len(content) < 20:
                #     continue
                json_obj = json.dumps(
                    {'text': content, 'deleted_image_count': image_count, 'd': json_obj['d']}, ensure_ascii=False)
                f2.write(json_obj)
                f2.write('\n')
                line = f1.readline()
                count += 1
                if count > 200:
                    break
