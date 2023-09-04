import json
import re

path = '/mnt/vepfs/lingxin/Pretrain-data/wulindong/sft_data/GAOKAO/gaokao.json'

with open(path,'r',encoding='utf-8')as file:
    all_data = file.readlines()

json_lines = map(json.loads,all_data)
pattern1 = r'^（.*?分）'
pattern2 = r'^\(.*?分\)'
pattern3 = r'^（.*?分\)'
result = []
for line in json_lines:
    
    text = line['dialog'][0]['input']
    text = text.strip()
    # text = re.sub(pattern1,'',text)
    text = re.sub(pattern2,'',text)
    text = text.strip()
    text = re.sub(pattern1,'',text)
    text = text.strip()
    text = re.sub(pattern3,'',text)
    line['dialog'][0]['input'] = text
    result.append(json.dumps(line,ensure_ascii=False))
with open("/mnt/vepfs/lingxin/Pretrain-data/wulindong/sft_data/GAOKAO/gaokao1.json",'w',encoding='utf-8')as file1:
    file1.write('\n'.join(result))

    