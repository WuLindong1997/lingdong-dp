python main_filtering_03.py \
        --dataset_path  /pretrain-data-bucket/pretrain_other/pretrain_else/weixin_page_dudmp_special_token_again_test500/weixin_page.2018_special_token_3000.jsonl\
        --lang_dataset_id zh \
        --path_sentencepiece_model /mnt/vepfs/lingxin/Pretrain-data/wulindong/code/dataprocessing-bigscience/zh.sp.model \
        --path_kenlm_model /mnt/vepfs/lingxin/Pretrain-data/wulindong/code/dataprocessing-bigscience/zh.arpa.bin \
        --remove_meta \
        --num_proc 50 \
        --path_dir_save_dataset /mnt/vepfs/lingxin/Pretrain-data/wulindong/bookdata/book_cache \

wait


