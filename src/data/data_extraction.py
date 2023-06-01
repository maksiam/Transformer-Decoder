# -*- coding: utf-8 -*-
import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
import pandas as pd
import click
import os
from PyPDF2 import PdfReader


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
    """Runs data processing scripts to turn epub and pdf books into parquet file DataFrame with text"""
    print("Start data extraction\n")
    # folder path
    hp_funfic = "hp_funfic"
    dir_path = input_filepath + hp_funfic +'/'

    # list file and directories
    books = os.listdir(dir_path)
    epub_dics = {title: [] for title in books}
    
    for title in books:
        book = epub.read_epub(dir_path + title)
        # get list of documents objects
        items = list(book.get_items_of_type(ebooklib.ITEM_DOCUMENT))
        for c in items:
            epub_dics[title].append(chapter_to_str(c))
        epub_dics[title] = " ".join(epub_dics[title])
    
    df = pd.DataFrame(epub_dics, index = ['text']).T
    # folder path
    hp_orig = "hp_original"
    dir_path = input_filepath + hp_orig +'/'

    # list file and directories
    books = os.listdir(dir_path)
    hp = {title: [] for title in books}
    for title in books:
        print(f"Reading {title}")
        # creating a pdf reader object
        reader = PdfReader(dir_path + title)

        # printing number of pages in pdf file
        print(f"Number of pages: {len(reader.pages)}")
        temp = []
        for page in reader.pages:
            text = page.extract_text()
            text = " ".join(text.split())
            temp.append(text)
        hp[title] = "\n".join(temp)
    df = pd.concat([df, pd.DataFrame(hp, index=["text"]).T], axis=0)
    df.to_parquet(output_filepath)
    print("Finish data extraction\n")


if __name__ == "__main__":
    main()
