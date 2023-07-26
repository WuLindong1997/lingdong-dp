#!/bin/bash
dataset_dir="/pretrain-data-bucket/pretrain_other/pretrain_else/weixin_page_dudmp_special_token_again_test500"
for file_path in ${dataset_dir}/*.jsonl; do
    python main_filtering_03.py \
        --dataset_path "${file_path}" \
        --lang_dataset_id zh \
        --path_sentencepiece_model /mnt/vepfs/lingxin/Pretrain-data/wulindong/code/dataprocessing-bigscience/zh.sp.model \
        --path_kenlm_model /mnt/vepfs/lingxin/Pretrain-data/wulindong/code/dataprocessing-bigscience/zh.arpa.bin \
        --remove_meta \
        --num_proc 70 \
        --path_dir_save_dataset /mnt/vepfs/lingxin/Pretrain-data/wulindong/code/bookcode/temp \

    wait
    filename=$(basename "$file_path")
    python filter_with_perplexity.py \
        --dataset_path /mnt/vepfs/lingxin/Pretrain-data/wulindong/code/bookcode/temp/zh \
        --save_path /pretrain-data-bucket/pretrain_other/pretrain_else/weixin_page_dudmp_special_token_again/$filename 
    rm -rf /mnt/vepfs/lingxin/Pretrain-data/wulindong/cache2/*
    rm -rf /mnt/vepfs/lingxin/Pretrain-data/wulindong/weixin_cache1/*
    rm -rf /mnt/vepfs/lingxin/Pretrain-data/wulindong/code/bookcode/temp/zh/*
done