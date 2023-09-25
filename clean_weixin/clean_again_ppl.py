import argparse
from bs4 import BeautifulSoup
import json
import re
from normalizations import normalizations
from tqdm import tqdm
import multiprocessing
import os
from functools import partial
import kenlm
import sentencepiece
from time import time
class ModifyingDocuments:
    @staticmethod
    def remove_empty_el_from_list(list_):
        return [el for el in list_ if el]

    @staticmethod
    def remove_non_printing_characters(document, non_printing_characters_re):
        return non_printing_characters_re.sub("", document)

    @staticmethod
    def uniform_whitespace(
        document,
        whitespace=[
            " ",
            " ",
            " ",
            " ",
            " ",
            "　",
            " ",
            " ",
            " ",
            " ",
            "￼",
            "",
        ],
    ):
        """There are different whitespace characters."""
        whitespace = set(whitespace)
        document = "".join(
            [char if char not in whitespace else " " for char in document]
        )
        return document

    @staticmethod
    def replace_digits_with_zeros(document, digits_re):
        return digits_re.sub("0", document)

    @staticmethod
    def replace_unicode_punctuation(document, unicode_punctuation):
        return "".join(unicode_punctuation.get(c, c) for c in document)

    @staticmethod
    def normalization(
        document,
        remove_non_printing_characters,
        strip,
        lower_case,
        uniform_whitespace,
        replace_digits_with_zeros,
        replace_unicode_punctuation,
        non_printing_characters_re=normalizations["non_printing_characters_re"],
        digits_re=normalizations["digits_re"],
        unicode_punctuation=normalizations["unicode_punctuation"],
    ):
        if remove_non_printing_characters:
            document = ModifyingDocuments.remove_non_printing_characters(
                document, non_printing_characters_re
            )
        if strip:
            document = document.strip()
        if not document:
            return document
        if lower_case:
            document = document.lower()
        if uniform_whitespace:
            document = ModifyingDocuments.uniform_whitespace(document)
        if replace_digits_with_zeros:
            document = ModifyingDocuments.replace_digits_with_zeros(document, digits_re)
        if replace_unicode_punctuation:
            document = ModifyingDocuments.replace_unicode_punctuation(
                document, unicode_punctuation
            )
        return document

    @staticmethod
    def tokenization(document, sentencepiece_model, join_on_whitespace):
        document_tokenized = sentencepiece_model.encode_as_pieces(document)
        if join_on_whitespace:
            document_tokenized = " ".join(document_tokenized)
        return document_tokenized

    @staticmethod
    def split_on_whitespace(
        document,
        new_line=False,
        tab=False,
    ):
        """This method also removes concatenated spaces."""
        sep = [" "] + new_line * ["\n"] + tab * ["\t"]
        sep = "|".join(sep)
        split_document = re.split(sep, document)
        split_document = ModifyingDocuments.remove_empty_el_from_list(split_document)
        return split_document

    @staticmethod
    def strip(document, strip_characters):
        """Way faster than document.strip(strip_characters)
        since strip_characters is now a set instead of a str,
        and it contains a lot of elements (all the emojis)."""
        if not document:
            return document
        beg_ind = 0
        end_ind = len(document)
        for i in range(len(document)):
            if document[i] in strip_characters:
                beg_ind += 1
            else:
                break
        for i in range(1, len(document) + 1):
            if document[-i] in strip_characters:
                end_ind -= 1
            else:
                break
        document_stripped = document[beg_ind:end_ind]
        return document_stripped

    @staticmethod
    def get_words_from_document(
        document, sentencepiece_model_tok, lower_case, strip_characters
    ):
        """Get words from a document. Non reversible since the document
        is split on multiple characters, words are stripped of
        special characters and characters are converted to lower case.
        Useful to compute ratios, like the stopwords ratio."""
        if sentencepiece_model_tok:
            document_normalized = ModifyingDocuments.normalization(
                document=document,
                remove_non_printing_characters=True,
                strip=True,
                lower_case=True,
                uniform_whitespace=True,
                replace_digits_with_zeros=True,
                replace_unicode_punctuation=True,
            )
            words = ModifyingDocuments.tokenization(
                document_normalized, sentencepiece_model_tok, join_on_whitespace=False
            )
        else:
            words = ModifyingDocuments.split_on_whitespace(
                document, new_line=True, tab=True
            )
        if lower_case:
            words = [word.lower() for word in words]
        if strip_characters:
            words = [ModifyingDocuments.strip(word, strip_characters) for word in words]
            words = ModifyingDocuments.remove_empty_el_from_list(words)
        return words

    @staticmethod
    def words_augmentation(words, group_size, join_char):
        """Augment words, especially for Chinese (without a space between words)
        and Vietnamese (with a space between syllables)."""
        augmentation = [
            join_char.join(words[i : i + group_size])
            for i in range(len(words) - group_size + 1)
        ]
        return augmentation

    @staticmethod
    def split_on_newline_tab_whitespace(document):
        """First split on "\n", then on "\t", then on " "."""
        sentences = document.split("\n")
        sentences = [sentence.split("\t") for sentence in sentences]
        sentences = [
            [
                ModifyingDocuments.split_on_whitespace(subsentence)
                for subsentence in sentence
            ]
            for sentence in sentences
        ]
        return sentences

    @staticmethod
    def merge_on_whitespace_tab_newline(sentences):
        """Invert the method split_on_newline_tab_whitespace.
        Removes concatenated separators."""
        sentences = [
            [" ".join(subsentence) for subsentence in sentence if subsentence]
            for sentence in sentences
        ]
        sentences = ["\t".join(sentence) for sentence in sentences if sentence]
        if not sentences:
            return ""
        document = "\n".join(sentences)
        return document

    @staticmethod
    def should_keep_word_with_incorrect_substrings(
        word, strip_characters, incorrect_word_substrings
    ):
        word = ModifyingDocuments.strip(word, strip_characters)
        should_keep = all(
            [(i_substr not in word) for i_substr in incorrect_word_substrings]
        )
        return should_keep

    @staticmethod
    def remove_words_with_incorrect_substrings(
        document,
        strip_characters,
        incorrect_word_substrings,
    ):
        sentences = ModifyingDocuments.split_on_newline_tab_whitespace(document)
        sentences = [
            [
                [
                    word
                    for word in subsentence
                    if ModifyingDocuments.should_keep_word_with_incorrect_substrings(
                        word, strip_characters, incorrect_word_substrings
                    )
                ]
                for subsentence in sentence
            ]
            for sentence in sentences
        ]
        document = ModifyingDocuments.merge_on_whitespace_tab_newline(sentences)
        return document

    @staticmethod
    def should_keep_long_word(word, strip_characters, length_word_max_cutoff):
        """If the word is too long but it contains only one
        special character, it might be a concatenation of one word,
        a punctuation, and another word, with no space between them.
        In this case, we give the word a pass."""
        if len(word) <= length_word_max_cutoff:
            return True
        word = ModifyingDocuments.strip(word, strip_characters)
        if not word:  # The word consisted only of strip characters
            return False
        if len(word) <= length_word_max_cutoff:
            return True
        return False

    def remove_long_words(
        document,
        strip_characters,
        length_word_max_cutoff,
    ):
        sentences = ModifyingDocuments.split_on_newline_tab_whitespace(document)
        sentences = [
            [
                [
                    word
                    for word in subsentence
                    if ModifyingDocuments.should_keep_long_word(
                        word,
                        strip_characters,
                        length_word_max_cutoff,
                    )
                ]
                for subsentence in sentence
            ]
            for sentence in sentences
        ]
        document = ModifyingDocuments.merge_on_whitespace_tab_newline(sentences)
        return document

    @staticmethod
    def modifying_documents(
        document,
        cond_uniform_whitespace,
        cond_replace_unicode_punctuation,
        cond_remove_words_with_incorrect_substrings,
        strip_characters,
        incorrect_word_substrings,
        cond_remove_long_words,
        length_word_max_cutoff,
    ):
        document = ModifyingDocuments.normalization(
            document=document,
            remove_non_printing_characters=False,
            strip=True,
            lower_case=False,
            uniform_whitespace=cond_uniform_whitespace,
            replace_digits_with_zeros=False,
            replace_unicode_punctuation=cond_replace_unicode_punctuation,
        )
        if cond_remove_words_with_incorrect_substrings:
            document = ModifyingDocuments.remove_words_with_incorrect_substrings(
                document,
                strip_characters,
                incorrect_word_substrings,
            )
        if cond_remove_long_words:
            document = ModifyingDocuments.remove_long_words(
                document,
                strip_characters,
                length_word_max_cutoff,
            )
        return document
       




def compute_perplexity_score(document, sentencepiece_model, kenlm_model):
        # document = ModifyingDocuments.normalization(
        #     document=document,
        #     remove_non_printing_characters=True,
        #     strip=True,
        #     lower_case=False,
        #     uniform_whitespace=True,
        #     replace_digits_with_zeros=True,
        #     replace_unicode_punctuation=True,
        # )
        document = ModifyingDocuments.tokenization(
            document, sentencepiece_model, join_on_whitespace=True
        )
        doc_log_score, doc_length = 0, 0
        for line in document.split("\n"):
            log_score = kenlm_model.score(line)
            length = len(line.split()) + 1
            doc_log_score += log_score
            doc_length += length
        pp_score = 10.0 ** (-doc_log_score / doc_length)
        pp_score = round(pp_score, 1)
        return pp_score


def process(data,kenlm_model,sentencepiece_model):
    # start_time = time()
    data = json.loads(data)['text']
    
    SPECIAL_TAG_FORMAT = {
        "code_block": r"\[CODE_START\](.*?)\[CODE_END\]",
        "code_inline": r"\[CODE_IN_START\](.*?)\[CODE_IN_END\]",
        "formula_block": r"\[EQ_START\](.*?)\[EQ_END\]",
        "formula_inline": r"\[EQ_IN_START\](.*?)\[EQ_IN_END\]",
        "img": r"\[IMG_START\](.*?)\[IMG_END\]",
        "table": r"\[TAB_START\](.*?)\[TAB_END\]",
        "emoji": r"\[EMJ_START\](.*?)\[EMJ_END\]",
    }
    patterns = [v for k, v in SPECIAL_TAG_FORMAT.items()]
    pattern = "|".join(patterns)
    
    cut_special_token_data = re.sub(pattern, "", data.replace("\n", " "))
    

    cond = True
    if kenlm_model:
        score = compute_perplexity_score(cut_special_token_data, sentencepiece_model, kenlm_model)
        cond = score <= args.perplexity_max_cutoff
        if cond:
            # end_time = time()
            # print(f'time:{end_time-start_time}')
            return json.dumps({"text":data,"remove":False},ensure_ascii=False)
        else:
            return json.dumps({"text":data,"remove":True},ensure_ascii=False)
    # end_time = time()
    # print(f'time:{end_time-start_time}')
    
    return 

def get_args():
    args_parser = argparse.ArgumentParser(description='parse_html')

    # dictionary or file
    args_parser.add_argument('--dataset_path', type=str,default='/mnt/vepfs/lingxin/Pretrain-data/wulindong/company_task/zhipu_api_task/novel_split_data')
    # args_parser.add_argument('--dataset_path', type=str,default='/pretrain-data-bucket/pretrain_other/pretrain_else/weixin_page_clean_special_token_other/weixin_page.2018-07-14')
    args_parser.add_argument('--save_path', type=str,default='/mnt/vepfs/lingxin/Pretrain-data/wulindong/company_task/zhipu_api_task/novel_split_data_ppl')
    args_parser.add_argument('--path_kenlm_model', type=str,default='/mnt/vepfs/lingxin/Pretrain-data/wulindong/lingdong-dp/clean_weixin/zh.arpa.bin')
    args_parser.add_argument('--path_sentencepiece_model', type=str,default='/mnt/vepfs/lingxin/Pretrain-data/wulindong/lingdong-dp/clean_weixin/zh.sp.model')
    args_parser.add_argument('--perplexity_max_cutoff', type=int,default=3000)
    args_parser.add_argument('--pool_num', type=int,default = 10)

    # parse
    args = args_parser.parse_args()

    return args

if __name__ == '__main__':
    # 1.args
    args = get_args()
    
    #loadding model
    kenlm_model = kenlm.Model(args.path_kenlm_model)
    sentencepiece_model = sentencepiece.SentencePieceProcessor()
    sentencepiece_model.load(args.path_sentencepiece_model)

    #loadding data file
    json_files = []
    save_files = []
    for root, dirs, files in os.walk(args.dataset_path):
        for file in files:
            if file.endswith('.jsonl') or file.endswith('.json'):
                json_files.append(os.path.join(root, file))
                save_files.append(os.path.join(args.save_path, file))

    #loadding dataset
    for path,save_path in zip(json_files,save_files):
        with open(path,'r',encoding='utf-8')as file:
            all_data = file.readlines()
        #设置一个偏函数
        process_data_partial = partial(process,kenlm_model = kenlm_model,sentencepiece_model = sentencepiece_model)

        #进行处理
        with multiprocessing.Pool(args.pool_num) as pool:
            results = pool.map_async(process_data_partial, all_data)
            results = results.get()  # 获取处理结果
        filtered_results = [r for r in results if r is not None]
        
        #save dataset
        print(f'saveing:{save_path}')
        with open(save_path,'w',encoding='utf-8')as file1:
            file1.write('\n'.join(filtered_results))


            
                
    
