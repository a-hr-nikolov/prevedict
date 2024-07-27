import shutil
from pathlib import Path

from processors import paths


def load_scraped(filepath: Path) -> list[tuple[str, str]]:
    scraped: list[tuple[str, str]] = []
    with open(filepath, encoding="utf-8") as scraped_file:
        lines = scraped_file.readlines()
        for i, line in enumerate(lines):
            if line == "\n":
                continue
            if line.startswith("["):
                scraped.append((lines[i - 1], line))

    return scraped


def replace_transcriptions(dict_path: Path, word_tuples: list[tuple[str, str]]) -> None:
    backup_name = dict_path.parent / dict_path.name + ".bak"
    shutil.copy2(dict_path, backup_name)

    with open(dict_path, mode="r+", encoding="utf-8") as d:
        dictionary = d.readlines()
        d.seek(0)

        # Since the scraping is based on the dict, it cannot contain words that are not
        # in the dict. Hence, no need to try/except the .index method. Also it's a bit
        # more efficient to not start it from the beginning on each word.
        start_idx = 0
        for w, t in word_tuples:
            replace_idx = dictionary.index(w, start_idx) + 1
            dictionary[replace_idx] = t
            start_idx = replace_idx + 1

        d.writelines(dictionary)


def main():
    en_bg_dict = paths.EN_BG_UTF
    scraped_file = paths.SCRAPED
    scraped_words = load_scraped(scraped_file)
    replace_transcriptions(en_bg_dict, scraped_words)


if __name__ == "__main__":
    main()
