#!/bin/bash
python /mnt/vepfs/lingxin/Pretrain-data/wulindong/text_dedup/minhash2.py \
    --path 11 \
    --output 11\
    --column text

wait
rm -rf /mnt/vepfs/lingxin/Pretrain-data/wulindong/weixin_cache/*