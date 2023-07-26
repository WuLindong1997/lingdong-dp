#!/bin/bash

for file in /pretrain-data-bucket/pretrain_other/pretrain_else/xiaohongshu_save_emoji_clean/*; do
    # 使用basename命令获取文件名部分
    filename_json=$(basename "$file")
    if [ -f "/pretrain-data-bucket/pretrain_other/pretrain_else/xiaohongshu_save_emoji_temp/$filename_json" ];
    then
        echo "/pretrain-data-bucket/pretrain_other/pretrain_else/xiaohongshu_save_emoji_temp/$filename_json exists. skip."
    else
        filename=$(basename "$file")
        #文档间去重
        python /mnt/vepfs/lingxin/pretrain/wulindong/code/dataprocessing-bigscience/preprocessing/training/01a_catalogue_cleaning_and_filtering/clean2.py \
            --dataset-path /pretrain-data-bucket/pretrain_other/pretrain_else/xiaohongshu_save_emoji_clean/$filename \
            --preprocessings dedup_document \
            --save-path /pretrain-data-bucket/pretrain_other/pretrain_else/xiaohongshu_dedup_document/$filename  \
            --save-to-json \
            --num-proc 18\
            --batch-size 128 
        wait
        echo "dedup_document ok!"
        rm -rf /mnt/vepfs/lingxin/pretrain/wulindong/cache2/*
        wait
        #文档间去重
        python /mnt/vepfs/lingxin/pretrain/wulindong/code/dataprocessing-bigscience/preprocessing/training/01a_catalogue_cleaning_and_filtering/clean2.py \
            --dataset-path /pretrain-data-bucket/pretrain_other/pretrain_else/xiaohongshu_dedup_document/$filename \
            --preprocessings dedup_document \
            --save-path /pretrain-data-bucket/pretrain_other/pretrain_else/xiaohongshu_save_emoji_temp/$filename  \
            --save-to-json \
            --num-proc 18 \
            --batch-size 128 
        wait
        echo "dedup_document ok!"
        rm -rf /mnt/vepfs/lingxin/pretrain/wulindong/cache2/*
        echo "rf cache1 ok!"
        wait
    fi
done
