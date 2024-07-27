VALID_NON_ALPHA_SYMBOLS = " -'"
CYRILLIC_RANGE = range(0x0400, 0x0500)
LATIN_RANGE = range(0x0041, 0x007B)


def is_cyrillic(text: str) -> bool:
    for char in text:
        is_invalid_char = (
            ord(char) not in CYRILLIC_RANGE and char not in VALID_NON_ALPHA_SYMBOLS
        )
        if is_invalid_char:
            return False
    return True


def is_latin(text: str) -> bool:
    for char in text:
        is_invalid_char = (
            ord(char) not in LATIN_RANGE and char not in VALID_NON_ALPHA_SYMBOLS
        )
        if is_invalid_char:
            return False
    return True
