#!/bin/bash
python /mnt/lingxin/Pretrain-data/wulindong/text_dedup/minhash2_2020.py \
    --path 11 \
    --output 11\
    --column text

wait
rm -rf /mnt/lingxin/Pretrain-data/wulindong/weixin_cache4/*