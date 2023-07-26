# created by leileqi
# to check the usage of sentence_piece_model and kenlm model
import sentencepiece
import kenlm
from filtering import ModifyingDocuments
path_sentencepiece_model = '/mnt/vepfs/lingxin/pretrain/wulindong/code/dataprocessing-bigscience/zh.sp.model'
path_kenlm_model = '/mnt/vepfs/lingxin/pretrain/wulindong/code/dataprocessing-bigscience/zh.arpa.bin'
lang_dataset_id = 'zh'
def load_sentencepiece_model(lang_dataset_id, path_sentencepiece_model):
    sentencepiece_lang_id = 'zh'
    # langs_id.loc[
    #     langs_id["dataset_id"] == lang_dataset_id, "sentencepiece_id"
    # ].iloc[0]
    if sentencepiece_lang_id:
        sentencepiece_model = sentencepiece.SentencePieceProcessor()
        sentencepiece_model.load(path_sentencepiece_model)
    else:
        sentencepiece_model = None
    return sentencepiece_model

def load_kenlm_model(lang_dataset_id, path_kenlm_model):
    kenlm_lang_id = 'zh'
    # langs_id.loc[
    #     langs_id["dataset_id"] == lang_dataset_id, "kenlm_id"
    # ].iloc[0]
    if kenlm_lang_id:
        kenlm_model = kenlm.Model(path_kenlm_model)
    else:
        kenlm_model = None
    return kenlm_model
sentencepiece_model = load_sentencepiece_model(lang_dataset_id, path_sentencepiece_model)
kenlm_model = load_kenlm_model(lang_dataset_id, path_kenlm_model)
def compute_perplexity_score(document, sentencepiece_model, kenlm_model):
    document = ModifyingDocuments.normalization(
        document=document,
        remove_non_printing_characters=True,
        strip=True,
        lower_case=False,
        uniform_whitespace=True,
        replace_digits_with_zeros=True,
        replace_unicode_punctuation=True,
    )
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
document = """
水)浑(水)楫(木)贾(水)笕(木)郊(木)捷(金)解(木)禁(木)靳(木)经(木)敬(木)靖(金)筠(木)琚(木)楷(木)蒯(木)琨(木)廓(木)雷(水)莉(木)里(火)廉(木)炼(火)粱(水)琳(木)零(火)旒(火)辂(火) ?(火)禄(火)路(火)湄(水) ?(水)盟(水) ?(水)莫(水)睦(火)乃(火)楠(木)农(火)暖(火)湃(水)逄(火)聘(水)莆(木)颀(木)琦(木)琪(木)祺(木)佥(木)铅(金)勤(木)诠(木)(木)群(木)裟(金)莎(木)诜(金)莘(木)圣(土)嵊(土)诗(金)轼(金)蜀(金)竖(木)嗣(金)肆(金)嵩(土)颂(木)肃(金)睢(金)绥(水)汤(水)塘(土)陀(火)琬(土)微(水) ?(水)炜(火)渭(水)温(土)渥(水)熙(水)苋(木)湘(水)详(金)想(金)新(金)歆(金)惺(金)绣(金)诩(土)煦(金)暄(金)煊(火)铉(金)渲(水)勋(土)询(金)琰(火)扬(火
"""
pp_score = compute_perplexity_score(document, sentencepiece_model, kenlm_model)
print(pp_score)