#!/bin/bash
for (( i=2127; i<=2592; i++ )); do
    gzip -d /mnt/vepfs/lingxin/pretrain/wulindong/baike/baike_$i.txt.gz
    echo "ungz baike_$i.txt.gz completed"
    python parse_html_pool.py --index $i
    echo "Task $i completed"
    rm -rf /mnt/vepfs/lingxin/pretrain/wulindong/baike/baike_$i.txt
    echo "rm baike_$i.txt completed"
    #文档内重复词去除
    python /mnt/vepfs/lingxin/pretrain/wulindong/code/dataprocessing-bigscience/preprocessing/training/01a_catalogue_cleaning_and_filtering/clean.py \
    	--dataset-path /mnt/vepfs/lingxin/pretrain/wulindong/baike_1/baike_$i.json \
    	--preprocessings dedup_template_soft \
    	--save-path /mnt/vepfs/lingxin/pretrain/wulindong/baike_2/baike_$i.json \
    	--save-to-json \
    	--num-proc 16 \
    	--batch-size 64
    rm -rf /mnt/vepfs/lingxin/pretrain/wulindong/cache/*
    echo "dedup_template_soft baike_$i.txt completed"
    python /mnt/vepfs/lingxin/pretrain/wulindong/code/filter_small_docs_toxic_words.py  --index $i
    echo "filter_small_docs_toxic_words.py   completed"
wait
echo $i completed
done
echo "All tasks completed"
