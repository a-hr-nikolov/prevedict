import pickle
from bisect import bisect_left
from dataclasses import dataclass
from pathlib import Path

from rapidfuzz import process

from prevedict.conf.paths import BG_EN_PKL, EN_BG_PKL
from prevedict.model import langcheck


@dataclass
class WordTranslation:
    word: str
    translation: str
    transcription: str = ""

    def __str__(self):
        if self.transcription != "":
            self.transcription += "\n"
        return self.word + "\n" + self.transcription + self.translation


class LanguageDict:
    def __init__(self, path: Path) -> None:
        self.translation_contents = self._load_dict(path)
        self.index = list(self.translation_contents.keys())

    @staticmethod
    def _load_dict(path: Path) -> dict[str, tuple[str, str]]:
        with path.open("rb") as p:
            return pickle.load(p)

    def get(self, word: str) -> WordTranslation | None:
        word = word.upper()
        word_tuple = self.translation_contents.get(word, None)
        if not word_tuple:
            return None
        return WordTranslation(word, word_tuple[0], word_tuple[1])

    def list_word_completions(self, fragment: str, limit: int = 100) -> list[str]:
        """
        A function that returns a list of words, which begin with the provided fragment,
        and where len(words) <= max <= 100.
        """
        if not fragment:
            return []

        fragment = fragment.upper()
        position = bisect_left(self.index, fragment)

        if position < 0 and position >= len(self.index):
            return []

        # first_candidate = self.words[index]
        candidates: list[str] = []
        limit = min(limit, 100)
        for candidate in self.index[position:]:
            if len(candidates) >= limit:
                break
            if not candidate.startswith(fragment):
                break
            candidates.append(candidate)

        return candidates

    def find_best_matches(self, term: str, limit: int = 100) -> list[str]:
        term = term.upper()
        extracted = process.extract(term, self.index, limit=150)
        matches = [
            (match, score) for match, score, _ in extracted if len(match) >= len(term)
        ]
        matches.sort(key=lambda x: (-x[1], len(x[0])))
        matches = [match for match, _ in matches]

        limit = min(len(matches), limit)

        return matches[:limit]


class Dictionary:
    def __init__(self) -> None:
        self.current_pack: LanguageDict = None
        self.bg_en = LanguageDict(BG_EN_PKL)
        self.en_bg = LanguageDict(EN_BG_PKL)

    def get(self, word: str) -> WordTranslation | None:
        if word is None:
            return None
        lang = self._determine_language(word)
        word_data = lang.get(word) if lang else None
        return word_data

    def list_word_completions(self, fragment: str, limit: int = 30) -> list[str]:
        """
        Returns a list of words starting with the supplied.
        """
        lang = self._determine_language(fragment)
        candidates = lang.list_word_completions(fragment, limit) if lang else []
        return candidates

    def find_best_matches(self, word: str, limit: int = 100) -> list[str]:
        lang = self._determine_language(word)
        matches = lang.find_best_matches(word, limit) if lang else None
        return matches

    def _determine_language(self, text: str) -> LanguageDict | None:
        if langcheck.is_latin(text):
            return self.en_bg
        if langcheck.is_cyrillic(text):
            return self.bg_en
        return None
