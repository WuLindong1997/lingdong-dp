import os
from tqdm import tqdm
import json
import re
import logging
def main():
    logger = logging.getLogger(__name__)   
    logging.basicConfig(
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
        datefmt="%m/%d/%Y %H:%M:%S",
        level=logging.INFO,
    )
    read_root_path = '/pretrain-data-bucket/pretrain_other/pretrain_else/xiaohongshu_save_emoji_cut'
    save_root_path = '/pretrain-data-bucket/pretrain_other/pretrain_else/xiaohongshu_save_emoji_end_again'
    list_path = []
    for file_name in os.listdir(read_root_path):
        list_path.append(os.path.join(read_root_path,file_name))
    
    for path in tqdm(list_path):

        save_path = os.path.join(save_root_path,path.split('/')[-1])
        if os.path.exists(save_path):
            logger.info(f'{path} exists so skip!')
            continue
        logger.info(f'processing {path}')
        result = []
        with open(path,'r',encoding='utf-8')as file:
            all_data = file.read().split('\n')
        for line in all_data:
            line_json = json.loads(line)
            #在这里加一个看前两句是否一样
            line_spl = line_json['text'].split('\n')
            if len(line_spl)>2:
                if line_spl[0] == line_spl[1]:
                    line_spl= line_spl[1:]
                    text = '\n'.join(line_spl)
                else:
                    text = line_json['text']
            else:
                text = line_json['text']
            text1 = re.sub(r'\[EMJ_START\].*?\[EMJ_END\]','',text)
                
            if len(text1) < 30:
                continue
            line_json['text'] = text
            result.append(json.dumps(line_json,ensure_ascii=False))

        logger.info(f'processed {path}')
        logger.info(f'processed ratio {(len(result)/len(all_data))*100}%')
        
        
        logger.info(f'saveing data to {save_path}')
        with open(save_path,'w',encoding='utf-8')as file1:
            file1.write('\n'.join(result))
        logger.info(f'save over to {save_path}')


if __name__ == "__main__":
    main()