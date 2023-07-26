for file in /pretrain-data-bucket/pretrain_other/pretrain_else/xiaohongshu_clean/*.json; do
    filename=$(basename "$file")
    python /mnt/vepfs/lingxin/pretrain/wulindong/code/xiaohongshu_code/xiaohongshu_clean_json2.py \
        --data_path $file \
        --save_path  /pretrain-data-bucket/pretrain_other/pretrain_else/xiaohongshu_end/$filename
    wait
    echo "$filename okkk!"
done