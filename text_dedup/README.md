# Text dedup


### 介绍
- 本代码可以用于数据的去重过滤工作

### 使用说明

~~~python
    ##修改下面的参数
    ##数据集目录
    args.path = '/mnt/vepfs/lingxin/Pretrain-data/wulindong/juben_crawl/dudmp_data'
    ##内容的key
    args.column = 'text'
    ##输出目录
    args.output = '/mnt/vepfs/lingxin/Pretrain-data/wulindong/juben_crawl/dudmp_data_exist'
    # args.output = '/mnt/vepfs/lingxin/Pretrain-data/leileqi_test/xiaohongshu_dedup_test/test_deduped'
    ##判定为重复文档的保存目录
    args.output_duped = '/mnt/vepfs/lingxin/Pretrain-data/wulindong/juben_crawl/dudmp_data_abandon'
    # args.output_duped = '/mnt/vepfs/lingxin/Pretrain-data/leileqi_test/xiaohongshu_dedup_test/test_deduped_abandoned'
    ##缓存目录
    args.cache_dir = '/mnt/vepfs/lingxin/Pretrain-data/wulindong/cache'
    # args.cache_dir = '/mnt/vepfs/lingxin/Pretrain-data/leileqi_test/xiaohongshu_dedup_test/test_cache'
    ##进程数
    args.num_proc = 30
    ##batch数d
    args.batch_size = 2000

    ################可调节的阈值##################
    args.num_perm = 10
    args.n_gram = 5
    # args.B = 10
    # args.R = 1
    args.threshold = 0.7
    args.false_positive_weight = 0.6
    args.false_negative_weight = 0.4
    ################可调节的阈值##################

~~~


### 测试去重效果调节
    - 执行/mnt/vepfs/lingxin/Pretrain-data/wulindong/lingdong-dp/text_dedup/test.ipynb
    - 查看假阳性的概率是多大