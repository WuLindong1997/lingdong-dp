"""Download Sentencepiece and KenLM models for supported languages.

Usage:
    python download_sentencepiece_kenlm_models.py --output_dir_path /tmp/

All Sentencepiece and KenLM language models will be saved under /tmp.
"""

import argparse
import subprocess

# from languages_id import langs_id
langs_id = {
        "lang": "Chinese",
        "dataset_id": "zh",
        "stopwords_id": "zh",
        "flagged_words_id": "zh",
        "fasttext_id": "zh",
        "sentencepiece_id": "zh",
        "kenlm_id": "zh",
    }


def download_sentencepiece_kenlm_models(output_dir_path: str) -> None:
        lang = "zh"
    # supported_sentencepiece_langs = langs_id["sentencepiece_id"].dropna().unique()
    # for lang in supported_sentencepiece_langs:
        try:
            output_sentencepiece = subprocess.check_output(
                f"wget https://huggingface.co/edugp/kenlm/resolve/main/wikipedia/{lang}.sp.model -P {output_dir_path}",  # http://dl.fbaipublicfiles.com/cc_net/lm/{lang}.sp.model for FB models
                shell=True,
            )
        except:
            print(
                f"Warning: Download failed for Sentencepiece model for language {lang}."
            )

    # supported_kenlm_langs = langs_id["kenlm_id"].dropna().unique()
    # for lang in supported_kenlm_langs:
    
        try:
            output_kenlm = subprocess.check_output(
                f"wget https://huggingface.co/edugp/kenlm/resolve/main/wikipedia/{lang}.arpa.bin -P {output_dir_path}",  # http://dl.fbaipublicfiles.com/cc_net/lm/{lang}.arpa.bin for FB models
                shell=True,
            )
        except:
            print(f"Warning: Download failed for KenLM model for language {lang}.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Download Sentencepiece and KenLM models for supported languages."
    )
    parser.add_argument(
        "--output_dir_path",
        type=str,
        default="/home/szt/zzh/LLM/dataprocessing-bigscience",
        help="Output directory path to save models.",
    )
    args = parser.parse_args()

    download_sentencepiece_kenlm_models(output_dir_path=args.output_dir_path)
