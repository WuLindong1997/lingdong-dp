for file in /mnt/vepfs/lingxin/pretrain/wulindong/baike/*.gz; do
    gzip -d "$file"
    echo "$file"ok
done
