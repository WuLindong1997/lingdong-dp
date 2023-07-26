import argparse
import json
import ast
import re


def get_data(data_path):
    with open(data_path,'r',encoding='utf-8') as file:
        list_text = file.read().split('\n')
    return list_text[:-1]


def re_clean(line):
    json_text = json.loads(line)
    text = json_text['text']
    #替换为2个以上个相同的标点符号
    #清除 @的对象和[]包含的东西以及#话题#删除
    pattern = r'_|つ|{}|（．＿．）|【】'
    text = re.sub(pattern, '', text, flags=re.DOTALL)
    text = text.replace('\n\n','\n')
    # 前后空格清除
    text = text.strip()
    text_dic = {}
    text_dic['text'] = text
    text_dic['liked_count'] = json_text['liked_count']
    text_dic['collected_count'] = json_text['collected_count']

    text = json.dumps(text_dic,ensure_ascii=False)
    return text,len(text_dic['text'])

def get_args():
    parser = argparse.ArgumentParser("clean xiaohongshu data")
    parser.add_argument('--data_path',type=str,default= './note_20230309.json')
    parser.add_argument('--save_path',type=str,default= './clean_note_20230309.json')
    return parser.parse_args()

def main():
    args = get_args()
    list_text = get_data(args.data_path)
    raw_total = len(list_text)
    result = []
    for line in list_text:
        text,length = re_clean(line)
        if length<25:  #为保证25个字符
            continue
        result.append(text)
    clean_over_total = len(result)
    #print(f'raw_total:{raw_total}\tclean_total:{clean_over_total}\tpercentage:{(clean_over_total/raw_total):.3f}% ')
    with open(args.save_path,'w',encoding='utf-8') as file:
        file.write('\n'.join(result))
if __name__ == '__main__':
    main()