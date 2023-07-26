#!/bin/bash
dataset_dir="/pretrain-data-bucket/pretrain_other/pretrain_else/weixin_page_dudmp_special_token_again_test500"
for file_path in ${dataset_dir}/*.jsonl; do
    file_name=$(basename "$file_path")
    python main_filtering_02.py \
        --dataset_path "${file_path}" \
        --lang_dataset_id zh \
        --path_sentencepiece_model /mnt/vepfs/lingxin/Pretrain-data/wulindong/code/dataprocessing-bigscience/zh.sp.model \
        --path_kenlm_model /mnt/vepfs/lingxin/Pretrain-data/wulindong/code/dataprocessing-bigscience/zh.arpa.bin \
        --remove_meta \
        --num_proc 30 \
        --path_dir_save_dataset /data \
        --save_path "/pretrain-data-bucket/pretrain_other/pretrain_else/weixin_page_dudmp_special_token_again/${file_name}"\

    rm -rf "/mnt/vepfs/lingxin/Pretrain-data/wulindong/bookdata/book_cache/*"
done