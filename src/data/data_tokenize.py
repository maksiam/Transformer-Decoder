# -*- coding: utf-8 -*-
import pandas as pd
from transformers import GPT2Tokenizer
import click


@click.command()
@click.argument("input_filepath", type=click.Path(exists=True))
@click.argument("output_filepath", type=click.Path())
def main(input_filepath: str, output_filepath: str):
    """Function for tokenizing our text

    Args:
        input_filepath (str): path to DataFrame with raw text
        output_filepath (str): path for saving DataFrame with tokenized data
    """
    df = pd.read_parquet(input_filepath)
    # loading tokenizer model
    model_name_or_path = "sberbank-ai/rugpt3large_based_on_gpt2"
    tokenizer = GPT2Tokenizer.from_pretrained(model_name_or_path)
    # tokenizing text
    encodes = []
    for paragraph in df.text:
        encodes.append(tokenizer.encode(paragraph, add_special_tokens=False))
    df['encode'] = encodes
    df.to_parquet(output_filepath)

if __name__ == "__main__":
    main()
