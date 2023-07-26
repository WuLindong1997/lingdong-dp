#!/bin/bash

for file in /pretrain-data-bucket/pretrain_other/pretrain_else/xiaohongshu/xhs_notes.2019-*.7z; do
    # 使用basename命令获取文件名部分
    filename_json=$(basename $file .7z).json
    if [ -f "/pretrain-data-bucket/pretrain_other/pretrain_else/xiaohongshu_clean/$filename_json" ];
    then
        echo "/pretrain-data-bucket/pretrain_other/pretrain_else/xiaohongshu_clean/$filename_json exists. skip."
    else
        7z x -o/mnt/vepfs/lingxin/pretrain/wulindong/xiaohongshu_un7z/ $file
        filename=$(basename "$file")
        #转json格式
        python /mnt/vepfs/lingxin/pretrain/wulindong/code/xiaohongshu_code/trans_json_pool_2019-05-24444.py \
            --data_path /mnt/vepfs/lingxin/pretrain/wulindong/xiaohongshu_un7z/${filename%.*} \
            --save_path /mnt/vepfs/lingxin/pretrain/wulindong/xiaohongshu_json/${filename%.*}.json 
        wait
        echo "trans json ok!"
        rm -rf /mnt/vepfs/lingxin/pretrain/wulindong/xiaohongshu_un7z/*
        wait
        #进行re正则清洗
        python /mnt/vepfs/lingxin/pretrain/wulindong/code/xiaohongshu_code/xiaohongshu_clean_json.py \
            --data_path /mnt/vepfs/lingxin/pretrain/wulindong/xiaohongshu_json/${filename%.*}.json \
            --save_path /mnt/vepfs/lingxin/pretrain/wulindong/xiaohongshu_1/${filename%.*}.json 	
        rm -rf /mnt/vepfs/lingxin/pretrain/wulindong/xiaohongshu_json/${filename%.*}.json
        echo "re ok!"
        #文档内重复词去除
        python /mnt/vepfs/lingxin/pretrain/wulindong/code/dataprocessing-bigscience/preprocessing/training/01a_catalogue_cleaning_and_filtering/clean.py \
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
        python /mnt/vepfs/lingxin/pretrain/wulindong/code/dataprocessing-bigscience/preprocessing/training/01a_catalogue_cleaning_and_filtering/clean.py \
            --dataset-path /mnt/vepfs/lingxin/pretrain/wulindong/xiaohongshu_2/${filename%.*}.json \
            --preprocessings dedup_document \
            --save-path /mnt/vepfs/lingxin/pretrain/wulindong/xiaohongshu_3/${filename%.*}.json \
            --save-to-json \
            --num-proc 10 \
            --batch-size 128 
        wait
        echo "dedup_document ok!"
        rm -rf /mnt/vepfs/lingxin/pretrain/wulindong/xiaohongshu_2/${filename%.*}.json
        rm -rf /mnt/vepfs/lingxin/pretrain/wulindong/cache/*
        echo "rf cache ok!"
        #ppl
        python /mnt/vepfs/lingxin/pretrain/wulindong/code/dataprocessing-bigscience/preprocessing/training/01b_oscar_cleaning_and_filtering/main_filtering_03.py \
            --dataset_path /mnt/vepfs/lingxin/pretrain/wulindong/xiaohongshu_3/${filename%.*}.json \
            --lang_dataset_id zh \
            --path_sentencepiece_model /mnt/vepfs/lingxin/pretrain/wulindong/code/dataprocessing-bigscience/zh.sp.model \
            --path_kenlm_model /mnt/vepfs/lingxin/pretrain/wulindong/code/dataprocessing-bigscience/zh.arpa.bin \
            --remove_meta \
            --num_proc 10 \
            --path_dir_save_dataset /mnt/vepfs/lingxin/pretrain/wulindong/xiaohongshu_4/  
        echo "ppl1 ok!"
        python /mnt/vepfs/lingxin/pretrain/wulindong/code/dataprocessing-bigscience/preprocessing/training/01b_oscar_cleaning_and_filtering/filter_with_perplexity.py\
            --dataset_path /mnt/vepfs/lingxin/pretrain/wulindong/xiaohongshu_4/zh \
            --save_path /mnt/vepfs/lingxin/pretrain/wulindong/xiaohongshu_5/${filename%.*}.json
        rm -rf /mnt/vepfs/lingxin/pretrain/wulindong/xiaohongshu_4/*
        mv /mnt/vepfs/lingxin/pretrain/wulindong/xiaohongshu_5/${filename%.*}.json /pretrain-data-bucket/pretrain_other/pretrain_else/xiaohongshu_clean
        rm -rf /mnt/vepfs/lingxin/pretrain/wulindong/cache_ppl2/*
        echo "ppl2 ok!"
        wait
    fi
done
