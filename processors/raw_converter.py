import re
from pathlib import Path

from processors import paths


def convert_bg_en(output_name: str):
    write_location = Path(__file__).parent / f"{output_name}.dat"
    with open(paths.BG_EN, mode="rb") as f, open(write_location, mode="wb") as nf:
        for line in f.readlines():
            new_line = line.replace(b"\x00", bytes("\n###\n", encoding="cp1251"))
            nf.write(new_line)

    print(f"{paths.BG_EN} converted to {write_location}")


def convert_en_bg(output_name: str):
    write_location = Path(__file__).parent / f"{output_name}.dat"
    with open(paths.BG_EN, mode="rb") as f, open(write_location, mode="wb") as nf:
        for line in f.readlines():
            new_line = line.replace(b"\x00", bytes("\n###\n", encoding="cp1251"))
            new_line = new_line.decode("cp1251")
            new_line = re.sub(r"]\s*", "]\n", new_line)
            new_line = new_line.encode("cp1251")
            nf.write(new_line)

    print(f"{paths.BG_EN} converted to {write_location}")


def to_utf(filepath: Path, output_name: str):
    write_location = Path(__file__).parent / f"{output_name}_utf.dat"
    with open(filepath, encoding="cp1251") as d, open(
        write_location, mode="w", encoding="utf-8"
    ) as nd:
        for c in d.read():
            nd.write(c)


def main():
    # new_bg_en = Path(__file__).parent / "bg_en_cp1251.dat"
    # new_en_bg = Path(__file__).parent / "en_bg_cp1251.dat"
    # remove_null(bg_en, "bg_en")
    # convert("bg_en")
    # convert("en_bg")
    to_utf(paths.BG_EN, "en_bg")
    to_utf(paths.EN_BG, "bg_en")


if __name__ == "__main__":
    main()
