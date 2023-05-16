# -*- coding: utf-8 -*-
import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
import pandas as pd


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


def main():
    """Runs data processing scripts to turn epub book into parquet file DataFrame with text"""
    book = epub.read_epub(r"data\raw\hpmor_ru.epub")
    # get list of documents objects
    items = list(book.get_items_of_type(ebooklib.ITEM_DOCUMENT))
    texts = {}
    for c in items:
        texts[c.get_name()] = chapter_to_str(c)
    df = pd.DataFrame(texts, index=["text"]).T
    df = df.iloc[3:-1]
    df.to_parquet(r"data\raw\hpmor_raw.parquet")


if __name__ == "__main__":
    main()
