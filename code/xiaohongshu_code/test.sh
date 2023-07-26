python /mnt/vepfs/lingxin/pretrain/wulindong/code/dataprocessing-bigscience/preprocessing/training/01b_oscar_cleaning_and_filtering/main_filtering.py \
        --dataset_path /mnt/vepfs/lingxin/pretrain/wulindong/xiaohongshu_3/note_20230309.json \
        --lang_dataset_id zh \
        --path_sentencepiece_model /mnt/vepfs/lingxin/pretrain/wulindong/code/dataprocessing-bigscience/zh.sp.model \
        --path_kenlm_model /mnt/vepfs/lingxin/pretrain/wulindong/code/dataprocessing-bigscience/zh.arpa.bin \
        --remove_meta \
        --num_proc 10 \
        --path_dir_save_dataset /mnt/vepfs/lingxin/pretrain/wulindong/xiaohongshu_4/ 