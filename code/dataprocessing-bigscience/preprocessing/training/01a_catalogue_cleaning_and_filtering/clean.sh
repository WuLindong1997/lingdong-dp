#!/bin/bash

for file_path in /data/pretrain/zhihu/zhihu_users_clean/*; do
    python clean.py \
        --dataset-path "$file_path" \
        --preprocessings dedup_document \
        --save-path "/data/pretrain/zhihu/zhihu_users_clean_dedup_document/$(basename ${file_path%.*})_clean.json" \
        --save-to-json \
        --num-proc 32 \
        --batch-size 128 &
    wait
    rm -rf /home/wulindong/.cache/huggingface/datasets
    echo "Cleaning complete:$file_path"
done

echo "All done."