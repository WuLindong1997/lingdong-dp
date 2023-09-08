import re
from typing import List, Pattern
from typing_extensions import Self
from dataclasses import dataclass
from functools import lru_cache

import hanzidentifier


class TagCleaner:
    TAGS = [
        ("[EMJ_START]", "[EMJ_END]"),  # emoji
        ("[IMG_START]", "[IMG_END]"),  # 图片
        ("[EQ_IN_START]", "[EQ_IN_END]"),  # 行内公式
        ("[CODE_IN_START]", "[CODE_IN_END]"),  # 行内代码
        ("[EQ_START]", "[EQ_END]"),  # 行间公式
        ("[CODE_START]", "[CODE_END]"),  # 代码块
        ("[TAB_START]", "[TAB_END]"),  # 表格
    ]

    @classmethod
    @lru_cache(maxsize=5)
    def get_instance(cls) -> Self:
        return cls()

    def __init__(self):
        self._patterns: List[Pattern] = []
        for tag_start, tag_end in self.TAGS:
            pattern = re.escape(tag_start) + r'(.|\n)*?' + re.escape(tag_end)
            self._patterns.append(re.compile(pattern))

    def remove_tags(self, text: str) -> str:
        """ 删除特殊标记 """
        for pattern in self._patterns:
            text = pattern.sub("", text)
        return text


def remove_tags(text: str) -> str:
    return TagCleaner.get_instance().remove_tags(text)


def is_md_title(line: str) -> bool:
    return re.match(r"^#+\s+.+", line.strip()) is not None


@dataclass
class Chapter:
    title: str
    content: str

    def is_useless_chapter(self) -> bool:
        """ 是否是"版权信息"等章节，这些章节需要被去掉 """
        for keyword in ("版权", "业界评论", "编著者", "合著者", "出版说明", "译者简介", "出版说明", "致谢", "参考文献", "编委会"):
            if keyword in self.title:
                return True
        if self.title.strip().strip('#').strip() == "" and '版' in self.content and 'ISBN' in self.content:
            return True
        return False

    @property
    def content_without_tags(self) -> str:
        return remove_tags(self.content)


def split_into_chapters(text: str) -> List[Chapter]:
    # 按markdown标题切分
    lines = text.splitlines()
    if not lines:
        return []

    chapters: List[Chapter] = []
    idx = 0
    if not is_md_title(lines[0]):
        first_chunk = []
        while idx < len(lines) and not is_md_title(lines[idx]):
            first_chunk.append(lines[idx])
            idx += 1
        chapters.append(Chapter(title='', content='\n'.join(first_chunk)))

    while idx < len(lines):
        assert is_md_title(lines[idx])
        title = lines[idx]
        idx += 1
        chunk = []
        while idx < len(lines) and not is_md_title(lines[idx]):
            chunk.append(lines[idx])
            idx += 1
        chapters.append(Chapter(title=title, content='\n'.join(chunk)))

    return chapters


def is_chinese_character(c: str):
    # 假设len(c) == 1
    # refs: https://stackoverflow.com/a/34587468
    return "\u4e00" <= c <= "\u9fff"


def are_chinese_characters_more_than_half(text: str):
    n_chinese_character = sum(is_chinese_character(c) for c in text)
    return n_chinese_character >= len(text) / 2


def are_traditional_chinese_characters_more_than_simplified(text: str):
    n_t = n_s = 0
    for c in text:
        if hanzidentifier.is_traditional(c):
            n_t += 1
        if hanzidentifier.is_simplified(c):
            n_s += 1
    return n_t > n_s


def split_to_sents(text: str, punctuations: str) -> List[str]:
    """ 切分成多个句子 """
    ps = re.escape(punctuations)
    pattern = rf"[^{ps}]*(?:[{ps}]+|$)"
    all_sents = []
    for line in text.splitlines():
        sents = [x for x in re.findall(pattern, line) if x]  # 上面的正则会额外匹配一个空字符串
        sents.append('\n')
        all_sents += sents
    return all_sents
