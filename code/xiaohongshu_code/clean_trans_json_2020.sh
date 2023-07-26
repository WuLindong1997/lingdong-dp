#!/bin/bash

for file in /pretrain-data-bucket/pretrain_other/pretrain_else/xiaohongshu/xhs_notes.2020-*.7z; do
    # 使用basename命令获取文件名部分
    filename_json=$(basename $file .7z).json
    #if [ -f "/pretrain-data-bucket/pretrain_other/pretrain_else/xiaohongshu_clean/$filename_json" ];
    if [ -f "/pretrain-data-bucket/pretrain_other/pretrain_else/xiaohongshu_save_emoji_json/$filename_json" ];
    then
        echo "/pretrain-data-bucket/pretrain_other/pretrain_else/xiaohongshu_save_emoji_json/$filename_json exists. skip."
    else
        echo $file  ziping!
        7z x $file -o/pretrain-data-bucket/pretrain_other/pretrain_else/xiaohongshu_json -mmt20
        filename=$(basename "$file")
        #转json格式
        python /mnt/vepfs/lingxin/pretrain/wulindong/code/xiaohongshu_code/trans_json_pool_2020.py \
            --data_path /pretrain-data-bucket/pretrain_other/pretrain_else/xiaohongshu_json/${filename%.*} \
            --save_path /pretrain-data-bucket/pretrain_other/pretrain_else/xiaohongshu_save_emoji_json/${filename%.*}.json 
        wait
        echo "trans json ok!"
        rm -rf /pretrain-data-bucket/pretrain_other/pretrain_else/xiaohongshu_json/*
        
    fi
done
