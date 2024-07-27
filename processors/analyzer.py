"""
A script I wrote for analyzing the transcriptions between the encodings. I figured I
would be able to use it as the basis for a translation table. However, it ultimately
made me realize that for some reason the raw data is interpreted completely incorrectly.

Instead of figuring out a programmatic solution to solve the encoding, I figured I can
just scrape the actual transcription with the correct symbols from the internet.

I am still leaving this script here for tracking purposes.
"""

from dataclasses import dataclass
from pathlib import Path

from processors import paths


@dataclass
class RawTranscription:
    word: str
    symbol: str
    transcription: str
    encoding: str


class Transcription:
    def __init__(self, raw: RawTranscription):
        self.encoding = raw.encoding
        self.word = raw.word
        self.symbol = raw.symbol
        self.symbol_bytes = self.symbol.encode(self.encoding)
        self.transcription = raw.transcription
        self.transcription_bytes = self.transcription.strip("[]").encode(self.encoding)

    def __str__(self):
        title_line = f"{self.word}\n"
        first_line = f"  {self.symbol}\tCODE: {self.symbol_bytes}\n"
        second_line = f"  {self.transcription}\n"
        third_line = f"  {self.transcription_bytes}\n"

        return title_line + first_line + second_line + third_line


def extract_raw_transcriptions(filepath: Path, encoding: str) -> list[RawTranscription]:
    tr_symbols = set()
    trs: list[RawTranscription] = []

    with open(filepath, mode="r", encoding=encoding) as d:
        lines = d.readlines()
        for i, line in enumerate(lines):
            if line[0] != "[":
                continue
            stripped_line = line.strip("\n[]")
            for c in stripped_line:
                if c in tr_symbols:
                    continue
                tr_symbols.add(c)
                trs.append(
                    RawTranscription(
                        word=lines[i - 1].strip(),
                        symbol=c,
                        transcription=line.strip(),
                        encoding=encoding,
                    )
                )

    return trs


def process_raw_transcriptions(raw: list[RawTranscription]):
    trs: list[Transcription] = []

    for rtr in raw:
        trs.append(Transcription(rtr))

    return trs


def compare_transcriptions(trs_utf: list[Transcription], trs_cp: list[Transcription]):
    trs = zip(trs_utf, trs_cp)
    for utf, cp in trs:
        if utf.symbol_bytes == cp.symbol_bytes:
            continue
        print(utf.word)
        print(
            f"UTF: {utf.symbol} {utf.symbol_bytes} | CP: {cp.symbol} {cp.symbol_bytes}"
        )
        print(f"UTF: {utf.transcription}\t{utf.transcription_bytes}")
        print(f"CP : {cp.transcription}\t{cp.transcription_bytes}\n")


def pprint(trs: list[Transcription]):
    for tr in trs:
        print(tr)


def main():
    en_bg = paths.EN_BG
    en_bg_utf = paths.EN_BG_UTF
    UTF = "utf-8"
    CP = "cp1251"

    raw_utf = extract_raw_transcriptions(en_bg_utf, UTF)
    raw_cp = extract_raw_transcriptions(en_bg, CP)
    processed_utf = process_raw_transcriptions(raw_utf)
    processed_cp = process_raw_transcriptions(raw_cp)
    # pprint(processed)
    compare_transcriptions(processed_utf, processed_cp)


if __name__ == "__main__":
    main()
