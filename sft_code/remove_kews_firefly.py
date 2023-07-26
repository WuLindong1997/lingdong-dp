import json

with open('/mnt/vepfs/lingxin/Pretrain-data/wulindong/sft_data/COIG-Chatgpt/human-value-alignment_special.json','r',encoding='utf-8')as file:
    all_data = file.readlines()

json_line = map(json.loads,all_data)

keys = ['文言文','上联','下联','对对子','诗']

result = []
for line in json_line:
    # flag = 1 
    # for word in keys:
    #     if word in line['dialog'][0]['input']:
    #         flag =0
    #         del line["chatgpt_output"]
    #         result.append(json.dumps(line,ensure_ascii=False))
    #         break
    # #如果没有出现诗，用chatgpt生成的
    # if flag == 1:
    #     line['dialog'][1]['output'] = line['chatgpt_output']
    #     del line['chatgpt_output']
    #     result.append(json.dumps(line,ensure_ascii=False))


    line['dialog'][1]['output'] = line['chatgpt_output']
    del line['chatgpt_output']
    result.append(json.dumps(line,ensure_ascii=False))

with open('/mnt/vepfs/lingxin/Pretrain-data/wulindong/sft_data/COIG-Chatgpt/human-value-alignment_special1.json','w',encoding='utf-8')as file1:
    file1.write('\n'.join(result))