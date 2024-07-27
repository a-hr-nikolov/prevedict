import sys
from pathlib import Path

### DIRS ###
try:
    MAIN_DIR = Path(sys._MEIPASS)  # PyInstaller necessity
except Exception:
    MAIN_DIR = Path(__file__).parent.parent
ASSETS_DIR = MAIN_DIR / "assets"
FONTS_DIR = ASSETS_DIR / "fonts"
ICONS_DIR = ASSETS_DIR / "icons"
DICTS_DIR = ASSETS_DIR / "dicts"

### PICKLED DICTS ###
BG_EN_PKL = DICTS_DIR / "dict_bg_en.pkl"
EN_BG_PKL = DICTS_DIR / "dict_en_bg.pkl"

### SETTINGS ###
SETTINGS = MAIN_DIR / "settings.json"
WINCONFIG = MAIN_DIR / "winconfig.json"

INFO_TEXT = ASSETS_DIR / "information_page.txt"

### ICONS ###
APP_ICON = ICONS_DIR / "globe-solid.png"
SETTINGS_ICON = ICONS_DIR / "gear-solid.png"
INFO_ICON = ICONS_DIR / "circle-info-solid.png"

### FONTS ###
NOTO_FONT = FONTS_DIR / "Noto_Sans" / "NotoSans-VariableFont_wdth,wght.ttf"
