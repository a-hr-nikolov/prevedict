"""
First, let's admire the filename.

Okay, now that we're done with that, this file is an attempt to load the dictionaries as
Python objects for potential easier future loading.
"""

import pickle
from collections import OrderedDict
from pathlib import Path

from processors import paths


def load_dict_file(path: Path) -> list[str]:
    dictionary: list[str] = []
    with path.open(encoding="utf-8") as d:
        dictionary = d.readlines()
    return dictionary


def convert_to_words(dictionary: list[str]) -> dict[str, tuple[str, str]]:
    """
    This conversion can be refactored in the following way, depending on the use case:
    1. tuple[str,str,str] - For a simple, space-efficient structure that is going to be
    bisected anyway.
    2. WordData(str,str,str) - A dataclass, with more general overhead. Personally, I
    think that it is better to construct the type when you need it, not ahead of time
    for every single word.

    The first option is fine, but it leaves the dictionary with bisection access only.
    This may or may not be fine, depending on the situation.
    """
    words: dict[str, tuple[str, str]] = {}
    current_word = None
    current_translation = ""
    current_transcription = ""
    for line in dictionary[2:]:
        if line.startswith("#"):
            words[current_word] = (current_translation, current_transcription)
            current_translation = ""
            current_transcription = ""
            current_word = None
            continue
        if line.startswith("["):
            current_transcription = line.strip()
            continue
        if line.isupper():
            current_word = line.strip()
            continue
        current_translation += line

    ordered_words = OrderedDict(sorted(words.items(), key=lambda item: item[0]))
    # Because the first appended word will always be "None" as of now
    return ordered_words


def pickle_dict(d: dict[str, tuple[str, str]], path: Path):
    with path.open("wb") as p:
        pickle.dump(d, p)


def main():
    bg_en_raw = load_dict_file(paths.BG_EN_UTF)
    en_bg_raw = load_dict_file(paths.EN_BG_UTF)

    bg_en_dict = convert_to_words(bg_en_raw)
    en_bg_dict = convert_to_words(en_bg_raw)

    pickle_dict(bg_en_dict, paths.BG_EN_PKL)
    pickle_dict(en_bg_dict, paths.EN_BG_PKL)


if __name__ == "__main__":
    main()
