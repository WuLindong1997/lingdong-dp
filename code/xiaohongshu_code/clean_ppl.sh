#!/bin/bash

for file in /pretrain-data-bucket/pretrain_other/pretrain_else/xiaohongshu_save_emoji_clean/*; do
    # 使用basename命令获取文件名部分
    filename_json=$(basename "$file")
    if [ -f "/pretrain-data-bucket/pretrain_other/pretrain_else/xiaohongshu_save_emoji_end/$filename_json" ];
    then
        echo "/pretrain-data-bucket/pretrain_other/pretrain_else/xiaohongshu_save_emoji_end/$filename_json exists. skip."
    else
        filename=$(basename "$file")
    
        #文档内重复词去除
        python /mnt/vepfs/lingxin/pretrain/wulindong/code/dataprocessing-bigscience/preprocessing/training/01a_catalogue_cleaning_and_filtering/clean1.py \
            --dataset-path /pretrain-data-bucket/pretrain_other/pretrain_else/xiaohongshu_save_emoji_clean/$filename \
            --preprocessings dedup_template_soft \
            --save-path /pretrain-data-bucket/pretrain_other/pretrain_else/xiaohongshu_dedup_template_soft/$filename \
            --save-to-json \
            --num-proc 10 \
            --batch-size 128
        echo "dedup_template_soft ok!"
        wait
        #文档间去重
        python /mnt/vepfs/lingxin/pretrain/wulindong/code/dataprocessing-bigscience/preprocessing/training/01a_catalogue_cleaning_and_filtering/clean2.py \
            --dataset-path /pretrain-data-bucket/pretrain_other/pretrain_else/xiaohongshu_dedup_template_soft/$filename \
            --preprocessings dedup_document \
            --save-path /pretrain-data-bucket/pretrain_other/pretrain_else/xiaohongshu_dedup_document/$filename  \
            --save-to-json \
            --num-proc 10 \
            --batch-size 128 
        wait
        echo "dedup_document ok!"
        rm -rf /mnt/vepfs/lingxin/pretrain/wulindong/cache2/*
        echo "rf cache1 ok!"
        #ppl
        python /mnt/vepfs/lingxin/pretrain/wulindong/code/dataprocessing-bigscience/preprocessing/training/01b_oscar_cleaning_and_filtering/main_filtering.py \
            --dataset_path /pretrain-data-bucket/pretrain_other/pretrain_else/xiaohongshu_dedup_document/$filename \
            --lang_dataset_id zh \
            --path_sentencepiece_model /mnt/vepfs/lingxin/pretrain/wulindong/code/dataprocessing-bigscience/zh.sp.model \
            --path_kenlm_model /mnt/vepfs/lingxin/pretrain/wulindong/code/dataprocessing-bigscience/zh.arpa.bin \
            --remove_meta \
            --num_proc 10 \
            --path_dir_save_dataset /pretrain-data-bucket/pretrain_other/pretrain_else/xiaohongshu_ppl/  
        echo "ppl1 ok!"
        python /mnt/vepfs/lingxin/pretrain/wulindong/code/dataprocessing-bigscience/preprocessing/training/01b_oscar_cleaning_and_filtering/filter_with_perplexity.py\
            --dataset_path /pretrain-data-bucket/pretrain_other/pretrain_else/xiaohongshu_ppl/zh \
            --save_path /pretrain-data-bucket/pretrain_other/pretrain_else/xiaohongshu_save_emoji_end/$filename
        rm -rf /pretrain-data-bucket/pretrain_other/pretrain_else/xiaohongshu_ppl/*
        rm -rf /mnt/vepfs/lingxin/pretrain/wulindong/cache_ppl/*
        echo "ppl2 ok!"
        wait
    fi
done
