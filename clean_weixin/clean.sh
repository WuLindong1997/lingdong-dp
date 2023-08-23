#!/bin/bash

for file in /pretrain-data-bucket/pretrain_other/pretrain_else/weixin/page/weixin_page.2020-*.7z; do
    # 使用basename命令获取文件名部分
    filename_d=$(basename $file .7z)
    if [ -d "/pretrain-data-bucket/pretrain_other/pretrain_else/weixin_page_clean/$filename_d" ];
    then
        echo "/pretrain-data-bucket/pretrain_other/pretrain_else/weixin_page_clean/$filename_json exists. skip."
    else
        mkdir /pretrain-data-bucket/pretrain_other/pretrain_else/weixin_page_clean/$filename_d
        7z x -o/pretrain-data-bucket/pretrain_other/pretrain_else/weixin_page_un7z $file -mmt20
        python /mnt/vepfs/lingxin/pretrain/wulindong/weixin_page/code/clean_weixin/parse_html_pool.py \
            --dataset_path   /pretrain-data-bucket/pretrain_other/pretrain_else/weixin_page_un7z/$filename_d \
            --save_path /pretrain-data-bucket/pretrain_other/pretrain_else/weixin_page_clean/$filename_d \
            --pool_num  20
        wait 
        rm -rf /pretrain-data-bucket/pretrain_other/pretrain_else/weixin_page_un7z/*

        
            
        
        
        
        
        
        # 7z x -o/mnt/vepfs/lingxin/pretrain/wulindong/xiaohongshu_un7z/ $file
        # filename=$(basename "$file")
        # #转json格式
        # python /mnt/vepfs/lingxin/pretrain/wulindong/code/xiaohongshu_code/trans_json_pool_2019-05-24444.py \
        #     --data_path /mnt/vepfs/lingxin/pretrain/wulindong/xiaohongshu_un7z/${filename%.*} \
        #     --save_path /mnt/vepfs/lingxin/pretrain/wulindong/xiaohongshu_json/${filename%.*}.json 
        # wait
        
    fi
done
