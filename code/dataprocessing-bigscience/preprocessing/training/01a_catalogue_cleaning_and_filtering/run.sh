# --dataset-path /home/szt/zzh/LLM/wudao/data.json \/home/zzh/llm/wudao/data.json
# scp -P 9000 zzh@10.249.45.38:/data/zzh/wudao/data.json /home/szt/zzh/LLM/wudao/
# wait
python clean.py \
    --dataset-path /home/szt/zzh/LLM/asc/data.json \
    --preprocessings dedup_document \
    --save-path /home/szt/zzh/LLM/asc/asc-v1.json \
    --save-to-json \
    --num-proc 32 \
    --batch-size 128 
wait
rm -rf /home/szt/.cache/huggingface/datasets
python clean.py \
    --dataset-path /home/szt/zzh/LLM/asc/asc-v1.json \
    --preprocessings dedup_template_soft \
    --save-path /home/szt/zzh/LLM/asc/asc-v2.json \
    --save-to-json \
    --num-proc 32 \
    --batch-size 128 
wait
rm -rf /home/szt/.cache/huggingface/datasets
