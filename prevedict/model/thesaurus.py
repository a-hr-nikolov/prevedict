import itertools
from urllib.parse import quote_plus

import httpx
from pydantic import BaseModel, HttpUrl, ValidationError
from pydantic_core import from_json

from prevedict.model import langcheck


class Definition(BaseModel):
    definition: str
    synonyms: list[str]
    antonyms: list[str]


class Meaning(BaseModel):
    partOfSpeech: str
    definitions: list[Definition]
    synonyms: list[str]
    # antonyms: list[str]


class License(BaseModel):
    name: str
    url: HttpUrl


class WordEntry(BaseModel):
    word: str
    phonetic: str
    meanings: list[Meaning]
    # license: License
    # sourceUrls: list[HttpUrl]


class WordDescription:
    def __init__(self, word_entries: list[WordEntry]) -> None:
        self.word = word_entries[0].word
        self.transcription = word_entries[0].phonetic
        meanings_lists = [item.meanings for item in word_entries]

        self.meanings = list(itertools.chain(*meanings_lists))


class Thesaurus:
    __THESAURUS_URL = "https://api.dictionaryapi.dev/api/v2/entries/en/"
    __SPELLING_URL = "https://api.datamuse.com/sug?s="

    @classmethod
    def get(cls, word: str) -> WordDescription | None:
        if not langcheck.is_latin(word):
            return None

        url = cls.__THESAURUS_URL + quote_plus(word)
        res_content = cls.__request_data(url)
        words = cls.__process_data(res_content)

        if not words:
            similar = cls.find_similar_words(word)

            for word in similar:
                url = cls.__THESAURUS_URL + quote_plus(word)
                res_content = cls.__request_data(url)
                words = cls.__process_data(res_content)

                if words:
                    break

        if not words:
            return None

        return WordDescription(words)

    @classmethod
    def find_similar_words(cls, word: str) -> list[str]:
        url = cls.__SPELLING_URL + word
        res_content = cls.__request_data(url)
        words = []
        LIMIT = 10

        for item in res_content:
            if len(words) >= LIMIT:
                break

            words.append(item["word"])

        return words

    @staticmethod
    def __request_data(url: str) -> list[dict[str]]:
        try:
            response = httpx.get(url)
            deserialized = from_json(response.content)
        except (
            httpx.RequestError,
            httpx.NetworkError,
            ValueError,
            httpx.TimeoutException,
        ):
            return []
        return deserialized

    @staticmethod
    def __process_data(data: list[dict[str]]) -> list[WordEntry]:
        words = []
        try:
            for word in data:
                words.append(WordEntry(**word))
        except (ValidationError, TypeError):
            pass
        return words
