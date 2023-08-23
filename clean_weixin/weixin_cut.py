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
    read_root_path = '/pretrain-data-bucket/pretrain_other/pretrain_else/xiaohongshu_save_emoji_end'
    save_root_path = '/pretrain-data-bucket/pretrain_other/pretrain_else/xiaohongshu_save_emoji_cut'
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
            text = re.sub(r'\[EMJ_START\].*?\[[EMJ_END]\]','',line_json['text'])
            if len(text) < 30:
                continue
            result.append(json.dumps(line_json,ensure_ascii=False))

        logger.info(f'processed {path}')
        logger.info(f'processed ratio {(len(result)/len(all_data))*100}%')
        
        
        logger.info(f'saveing data to {save_path}')
        with open(save_path,'w',encoding='utf-8')as file1:
            file1.write('\n'.join(result))
        logger.info(f'save over to {save_path}')


if __name__ == "__main__":
    main()