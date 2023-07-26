#!/bin/bash

for file in /pretrain-data-bucket/pretrain_other/pretrain_else/xiaohongshu/xhs_notes.2021*.7z; do
    # 使用basename命令获取文件名部分
    7z x -o/mnt/vepfs/lingxin/pretrain/wulindong/xiaohongshu_un7z1/ $file
    filename=$(basename "$file")
    #转json格式
    python /mnt/vepfs/lingxin/pretrain/wulindong/code/xiaohongshu_code/trans_json_pool_01.py \
    	--data_path /mnt/vepfs/lingxin/pretrain/wulindong/xiaohongshu_un7z1/${filename%.*} \
    	--save_path /mnt/vepfs/lingxin/pretrain/wulindong/xiaohongshu_json/${filename%.*}.json 
    wait
    echo "trans json ok!"
    rm -rf /mnt/vepfs/lingxin/pretrain/wulindong/xiaohongshu_un7z1/*
    wait
    #进行re正则清洗
    python /mnt/vepfs/lingxin/pretrain/wulindong/code/xiaohongshu_code/xiaohongshu_clean_json.py \
    	--data_path /mnt/vepfs/lingxin/pretrain/wulindong/xiaohongshu_json/${filename%.*}.json \
    	--save_path /mnt/vepfs/lingxin/pretrain/wulindong/xiaohongshu_1/${filename%.*}.json 	
    rm -rf /mnt/vepfs/lingxin/pretrain/wulindong/xiaohongshu_json/${filename%.*}.json
    echo "re ok!"
    #文档内重复词去除
    python /mnt/vepfs/lingxin/pretrain/wulindong/code/dataprocessing-bigscience/preprocessing/training/01a_catalogue_cleaning_and_filtering/clean1.py \
    	--dataset-path /mnt/vepfs/lingxin/pretrain/wulindong/xiaohongshu_1/${filename%.*}.json \
    	--preprocessings dedup_template_soft \
    	--save-path /mnt/vepfs/lingxin/pretrain/wulindong/xiaohongshu_2/${filename%.*}.json \
    	--save-to-json \
    	--num-proc 10 \
    	--batch-size 128
    echo "dedup_template_soft ok!"
    wait
    rm -rf /mnt/vepfs/lingxin/pretrain/wulindong/xiaohongshu_1/${filename%.*}.json
    #文档间去重
    python /mnt/vepfs/lingxin/pretrain/wulindong/code/dataprocessing-bigscience/preprocessing/training/01a_catalogue_cleaning_and_filtering/clean1.py \
        --dataset-path /mnt/vepfs/lingxin/pretrain/wulindong/xiaohongshu_2/${filename%.*}.json \
        --preprocessings dedup_document \
        --save-path /mnt/vepfs/lingxin/pretrain/wulindong/xiaohongshu_3/${filename%.*}.json \
        --save-to-json \
        --num-proc 10 \
        --batch-size 128 
    wait
    echo "dedup_document ok!"
    rm -rf /mnt/vepfs/lingxin/pretrain/wulindong/xiaohongshu_2/${filename%.*}.json
    rm -rf /mnt/vepfs/lingxin/pretrain/wulindong/cache1/*
    echo "rf cache1 ok!"
    #ppl
    python /mnt/vepfs/lingxin/pretrain/wulindong/code/dataprocessing-bigscience/preprocessing/training/01b_oscar_cleaning_and_filtering/main_filtering_02.py \
        --dataset_path /mnt/vepfs/lingxin/pretrain/wulindong/xiaohongshu_3/${filename%.*}.json \
        --lang_dataset_id zh \
        --path_sentencepiece_model /mnt/vepfs/lingxin/pretrain/wulindong/code/dataprocessing-bigscience/zh.sp.model \
        --path_kenlm_model /mnt/vepfs/lingxin/pretrain/wulindong/code/dataprocessing-bigscience/zh.arpa.bin \
        --remove_meta \
        --num_proc 10 \
        --path_dir_save_dataset /mnt/vepfs/lingxin/pretrain/wulindong/xiaohongshu_6/  
    echo "ppl1 ok!"
    python /mnt/vepfs/lingxin/pretrain/wulindong/code/dataprocessing-bigscience/preprocessing/training/01b_oscar_cleaning_and_filtering/filter_with_perplexity.py\
        --dataset_path /mnt/vepfs/lingxin/pretrain/wulindong/xiaohongshu_6/zh \
        --save_path /mnt/vepfs/lingxin/pretrain/wulindong/xiaohongshu_5/${filename%.*}.json
    rm -rf /mnt/vepfs/lingxin/pretrain/wulindong/xiaohongshu_6/*
    mv /mnt/vepfs/lingxin/pretrain/wulindong/xiaohongshu_5/${filename%.*}.json /pretrain-data-bucket/pretrain_other/pretrain_else/xiaohongshu_clean
    echo "ppl2 ok!"
    wait
    rm -rf /home/wulindong/.cache/huggingface/*
    rm -rf /mnt/vepfs/lingxin/pretrain/wulindong/cache_ppl1/*
done
