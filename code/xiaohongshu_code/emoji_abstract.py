import re
import emoji
import argparse
import multiprocessing
from tqdm import tqdm
import json

def get_args():
    parser = argparse.ArgumentParser("clean xiaohongshu data")
    parser.add_argument('--data_path',type=str,default= '/pretrain-data-bucket/pretrain_other/pretrain_else/xiaohongshu_save_emoji_json/note_20230309.json')
    parser.add_argument('--save_path',type=str,default= './1.json')
    return parser.parse_args()

def get_data(path):
    with open(path,'r',encoding='utf-8')as file1:
        data = file1.read().split('\n')
    return data


def process(json_text):

    json_line = json.loads(json_text)
    text = json_line['text']


    # 定义包含指定表情的正则表达式
    emoji_pattern = emoji.emoji_pattern
    pattern = r'[^\u4e00-\u9fa5a-zA-Z0-9，。！？、；：“”‘’（）#,.:;《》\s😀-🙏🌀-🗿🚀-\U0001f6ff\U0001f1e0-🇿]'

    text = re.sub(pattern,'',text,flags=re.DOTALL)
    processed_text = re.sub(emoji_pattern, lambda m: f"[EMJ_START]{m.group()}[EMJ_END]", text)
    json_line['text'] = processed_text

    return json.dumps(json_line,ensure_ascii=False)

if __name__ == '__main__':
    args = get_args()
    data = get_data(args.data_path)
    with multiprocessing.Pool(1) as pool:
        result = list(tqdm(pool.imap_unordered(process, data), total=len(data)))
    with open(args.save_path,'w',encoding='utf-8') as file2:
        file2.write('\n'.join(result))
    print(f'保存成功\t{args.save_path}')

