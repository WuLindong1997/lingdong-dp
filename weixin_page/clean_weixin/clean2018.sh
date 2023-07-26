#!/bin/bash

for file in /pretrain-data-bucket/pretrain_other/pretrain_else/weixin/page/weixin_page.2018-{01,02,03,04,05,06,07,08}*.7z; do
    # 使用basename命令获取文件名部分
    filename_d=$(basename $file .7z)
    if [ -d "/pretrain-data-bucket/pretrain_other/pretrain_else/weixin_page_clean_special_token_other/$filename_d" ];
    then
        echo "/pretrain-data-bucket/pretrain_other/pretrain_else/weixin_page_clean_special_token_other/$filename_d exists. skip."
    else
        7z x -o/pretrain-data-bucket/pretrain_other/pretrain_else/weixin_page_un7z2018 $file -mmt20
        echo '7z解压！！！！'
        mkdir /pretrain-data-bucket/pretrain_other/pretrain_else/weixin_page_clean_special_token_other/$filename_d


        python /mnt/vepfs/lingxin/Pretrain-data/wulindong/weixin_page/code/clean_weixin/parse_html_pool_2018.py \
            --dataset_path   /pretrain-data-bucket/pretrain_other/pretrain_else/weixin_page_un7z2018/$filename_d \
            --save_path /pretrain-data-bucket/pretrain_other/pretrain_else/weixin_page_clean_special_token_other/$filename_d \
	        --batch_size 100000000\
            --pool_num  30
        wait
        rm -rf /pretrain-data-bucket/pretrain_other/pretrain_else/weixin_page_un7z2018/*


        # 7z x -o/mnt/vepfs/lingxin/pretrain/wulindong/xiaohongshu_un7z/ $file
        # filename=$(basename "$file")
        # #转json格式
        # python /mnt/vepfs/lingxin/pretrain/wulindong/code/xiaohongshu_code/trans_json_pool_2019-05-24444.py \
        #     --data_path /mnt/vepfs/lingxin/pretrain/wulindong/xiaohongshu_un7z/${filename%.*} \
        #     --save_path /mnt/vepfs/lingxin/pretrain/wulindong/xiaohongshu_json/${filename%.*}.json
        # wait

    fi
done
