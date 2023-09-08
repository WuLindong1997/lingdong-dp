import json
import math
from pathlib import Path
from collections import Counter
from typing import List, Iterator, Optional
import os
from tqdm import tqdm
from multiprocessing import Pool

from utils import split_into_chapters, are_chinese_characters_more_than_half, \
    are_traditional_chinese_characters_more_than_simplified, split_to_sents


def split_into_max_length(chapter_content: str, max_doc_length: int) -> Iterator[str]:
    if are_traditional_chinese_characters_more_than_simplified(chapter_content):
        return
    if math.isinf(max_doc_length):
        yield chapter_content
        return

    sents = []
    total_length = 0

    def concat():
        nonlocal total_length
        # split_to_sents 处理了换行符，用''.join即可
        r = ''.join(sents)
        sents.clear()
        total_length = 0
        return r

    for sent in split_to_sents(chapter_content, "。？?！!"):
        if not sent:
            continue
        if total_length + len(sent) <= max_doc_length:
            sents.append(sent)
            total_length += len(sent)
            continue

        assert total_length <= max_doc_length
        if sents:
            yield concat()

        if len(sent) <= max_doc_length:
            sents.append(sent)
            total_length += len(sent)
        else:
            # 一般单个句子不会超过最大长度，这里简单切分即可
            yield sent[: max_doc_length]

    if sents:
        yield concat()


def process_text(raw_text: str, max_doc_length: int) -> Iterator[str]:
    if not are_chinese_characters_more_than_half(raw_text):
        return
    for chapter in split_into_chapters(raw_text):
        if chapter.is_useless_chapter():
            continue
        yield from split_into_max_length(chapter.content_without_tags, max_doc_length)


def process_file(input_file: Path, output_file: Path, max_doc_length: int):
    raw_text = input_file.read_text().strip()
    with open(output_file, 'w', encoding='utf-8') as writer:
        for chunk in process_text(raw_text, max_doc_length):
            json.dump({"text": chunk.strip()}, writer, ensure_ascii=False)
            writer.write("\n")


def _recursive_walk(p: Path, visited: Optional[set] = None):
    if visited is None:
        visited = set()

    p = p.absolute().resolve()
    if p not in visited:
        visited.add(p)
    else:
        return

    if p.is_file():
        yield p
    elif p.is_dir():
        for f in p.glob("*"):
            yield from _recursive_walk(f, visited)


def find_markdown(input_dir: str):
    for file in _recursive_walk(Path(input_dir)):
        if file.suffix.lower() == '.md':
            yield file


# "情感小说"  ?
# categories: List[str] = ["哲学", "心理", "个人成长", "伦理学"]


def main(input_dir: str, output_dir: str, max_doc_length: str):
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    if max_doc_length == 'inf':
        max_doc_length = float("inf")
    else:
        max_doc_length = int(max_doc_length)
    name_count = Counter()
    md_files = list(find_markdown(input_dir))
    # md_files = [file for file in md_files if any(cate in file.absolute().parent.name for cate in categories)]
    for file in md_files:
        name_count[file.name] += 1
        n = name_count[file.name]
        name = file.stem + '.jsonl'
        if n > 1:
            # name = name + f"_{n}"
            continue
        output_file = Path(output_dir) / name
        process_file(file, output_file, max_doc_length=max_doc_length)

def process_directory(input_dir, output_dir):
    main(input_dir, output_dir, 'inf')

if __name__ == "__main__":
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument("--max_doc_length", default= 'inf')
    args = parser.parse_args()
    print(args)
    with open('/mnt/vepfs/lingxin/Pretrain-data/wulindong/markdown_process/code/file_path.json','r',encoding="utf-8")as file:
        file_names = json.loads(file.read())
    
    save_root = "/mnt/vepfs/lingxin/Pretrain-data/wulindong/markdown_process/data/markdown"
    list_input = []
    list_output = []
    for file_name,file_path in file_names.items():

        list_input.append(file_path)
        list_output.append(os.path.join(save_root,file_name))
        
    pool = Pool(20)
    for input_dir, output_dir in tqdm(zip(list_input, list_output), total=len(list_input)):
    # 使用进程池异步执行process_directory函数
        pool.apply_async(process_directory, args=(input_dir, output_dir))

    pool.close()

    # 等待所有进程完成
    pool.join()