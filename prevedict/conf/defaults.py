from prevedict.conf import const


def __generate_font_details(size: int, style: str = "Regular") -> dict[str]:
    return {"name": const.DEFAULT_FONT_NAME, "style": style, "size": size}


SETTINGS = {
    "behavior": {
        "list_limit": 50,
    },
    "display": {
        "language": "English",
        "theme": "Default",
    },
    "fonts": {
        "general": __generate_font_details(12),
        "input": __generate_font_details(12),
        "heading": __generate_font_details(14, "Bold"),
        "transcription": __generate_font_details(12, "Light"),
        "word_list": __generate_font_details(10),
    },
}

WINCONFIG = {
    "main_window": {
        "maximized": False,
        "geometry": [0, 0, 800, 600],
    },
    "splitter": {
        "proportions": [1, 3],
    },
}
