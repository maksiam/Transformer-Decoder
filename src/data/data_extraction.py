# -*- coding: utf-8 -*-
import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
import pandas as pd
import click


def chapter_to_str(chapter: str) -> str:
    """Function for html parsing epub file into text

    Args:
        chapter (str): chapter object

    Returns:
        str: text of the chapter
    """
    soup = BeautifulSoup(chapter.get_body_content(), "html.parser")
    text = [para.get_text() for para in soup.find_all("p")]
    return " ".join(text)


@click.command()
@click.argument("input_filepath", type=click.Path(exists=True))
@click.argument("output_filepath", type=click.Path())
def main(input_filepath: str, output_filepath: str):
    """Runs data processing scripts to turn epub book into parquet file DataFrame with text"""
    print('Start data extraction\n')
    book = epub.read_epub(input_filepath)
    # get list of documents objects
    items = list(book.get_items_of_type(ebooklib.ITEM_DOCUMENT))
    texts = {}
    for c in items:
        texts[c.get_name()] = chapter_to_str(c)
    df = pd.DataFrame(texts, index=["text"]).T
    df = df.iloc[3:-1]
    df.to_parquet(output_filepath)
    print('Finish data extraction\n')


if __name__ == "__main__":
    main()