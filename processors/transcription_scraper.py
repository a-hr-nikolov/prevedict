"""
A tool for scraping https://slovored.com/search/english/{word}, and extracting its
transcription field.
"""

import sys
import time
from pathlib import Path
from urllib.parse import quote_plus

import requests
from bs4 import BeautifulSoup

from processors import paths


def scrape_transcription(word: str):
    url = f"https://slovored.com/search/english/{quote_plus(word)}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    transcriptions = soup.find_all("span", class_="transcription")
    return transcriptions[0].text


def load_from_dat(dict_path: Path, encoding: str) -> list[str]:
    lines = []
    with open(dict_path, encoding=encoding) as d:
        lines = d.readlines()
    return lines


def extract_words(dictionary: list[str]) -> list[str]:
    words: list[tuple[str, str]] = []

    for i, line in enumerate(dictionary):
        if line[0] != "[":
            continue
        # transcription = line.strip()
        word = dictionary[i - 1].strip()
        words.append(word)

    return words


def scrape_and_save():
    dictionary = load_from_dat(paths.EN_BG_UTF, "utf-8")
    words = extract_words(dictionary)

    scraped_file_path = paths.SCRAPED
    failed_file_path = paths.SCRAPED_FAILED

    with open(scraped_file_path, mode="r+", encoding="utf-8") as scraped_file, open(
        failed_file_path, mode="a", encoding="utf-8"
    ) as failed_file:
        scraped_lines: list[str] = scraped_file.readlines()
        start_index = 0

        possible_empty_lines_counts = 3
        if len(scraped_lines) > possible_empty_lines_counts:
            last_scraped = ""
            for line in reversed(scraped_lines):
                line = line.strip()
                if line.isupper():
                    last_scraped = line
                    break

            start_index = 0
            try:
                start_index = words.index(last_scraped) + 1
                print(
                    f"Last scraped item: {last_scraped.strip()}\nStarting scraping from item #{start_index+1}"
                )
            except ValueError:
                print("Scraped file not empty, but no dictionary word found")
                raise

        words_left = words[start_index:]
        for i, w in enumerate(words_left):
            print(f"\rProcessing item {i} of {len(words_left)}", end="")
            try:
                tr = scrape_transcription(w)
            except IndexError:
                failed_file.write(f"{w}\n")
                print(f"\nFAILED SCRAPE:  {w}")
            except requests.exceptions.ConnectionError:
                failed_file.write(f"{w}\n")
                print(f"\nFAILED SCRAPE:  {w}")
                time.sleep(30)
            scraped_file.write(f"{w}\n{tr}\n\n")
            sys.stdout.flush()
        print("Scraping completed!")


if __name__ == "__main__":
    scrape_and_save()
