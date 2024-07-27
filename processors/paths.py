from pathlib import Path

### DIRECTORIES ###
PROCESSORS_DIR = Path(__file__).parent
DATA_DIR = PROCESSORS_DIR / "data"
PKL_DIR = PROCESSORS_DIR.parent / "en_bg_dict" / "assets"


### PICKLED DICTS ###
BG_EN_PKL = PKL_DIR / "dict_bg_en.pkl"
EN_BG_PKL = PKL_DIR / "dict_en_bg.pkl"


### DICTIONARY DATA ###
BG_EN = PKL_DIR / "bg_en.dat"
BG_EN_CP = DATA_DIR / "bg_en_cp.dat"
BG_EN_UTF = DATA_DIR / "bg_en_utf.dat"

EN_BG = DATA_DIR / "en_bg.dat"
EN_BG_CP = DATA_DIR / "en_bg_cp.dat"
EN_BG_UTF = DATA_DIR / "en_bg_utf.dat"

### PROCESSOR PRODUCTS ###
SCRAPED = PROCESSORS_DIR / "scraped.txt"
SCRAPED_FAILED = PROCESSORS_DIR / "scraped_failed.txt"
CORRECTED = PROCESSORS_DIR / "corrected.txt"
