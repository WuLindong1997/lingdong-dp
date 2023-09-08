import json
import os
from pathlib import Path
from argparse import ArgumentParser
from typing import Optional
from tqdm import tqdm


def recursive_walk(p: Path, seen: Optional[set] = None):
    if seen is None:
        seen = set()
    
    p = p.absolute().resolve()
    if p in seen:
        return
    else:
        seen.add(p)
    
    if p.is_file():
        yield p
    elif p.is_dir():
        for sub_p in p.glob("*"):
            yield from recursive_walk(sub_p, seen=seen)


def main(name_file: str, data_dir: str, output_file: str, cache_dir: str):
    # read file names
    with open(name_file, 'r', encoding='utf-8') as reader:
        names = [x for x in reader.read().strip().splitlines() if x]
    
    # list all data files
    cache_file = Path(cache_dir) / (data_dir.strip(os.sep).replace(os.sep, '+') + '.json')
    if cache_file.is_file():
        with open(cache_file, 'r', encoding='utf-8') as f:
            all_files = json.load(f)
    else:
        all_files = {p.stem: str(p) for p in tqdm(recursive_walk(Path(data_dir)))}
        cache_file.absolute().parent.mkdir(parents=True, exist_ok=True)
        with open(cache_file, 'w', encoding='utf-8') as writer:
            json.dump(all_files, writer, indent=4, ensure_ascii=False)
            
    # find files with specified name
    found_files = {name: str(all_files[name]) for name in names if name in all_files}
    
    print(f"#names: {len(names)}")
    print(f"#files: {len(all_files)}")
    print(f"#found_files: {len(found_files)}")
    
    Path(output_file).absolute().parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as writer:
        json.dump(found_files, writer, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--name_file", required=True)
    parser.add_argument("--data_dir", required=True)
    parser.add_argument("--output_file", required=True)
    parser.add_argument("--cache_dir", default='/mnt/vepfs/lingxin/Pretrain-data/wulindong/cache')
    args = parser.parse_args()
    main(**vars(args))
