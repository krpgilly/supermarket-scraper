import re
import unicodedata

DAIRY_WORDS = [
    "milk", "cheese", "cheddar", "butter", "buttersoft", "yogurt", "yoghurt",
    "eggs", "brie", "mozzarella", "feta", "halloumi",
    "parmesan", "parmigiano",  "double cream", "single cream", "whipping cream",
    "creme fraiche", "dairy drink",
]

NOT_DAIRY_WORDS = [
    "tart", "tarts", "quiche", "pasty", "pastry", "pie", "pies",
    "baguette", "tortelloni", "ravioli", "pasta", "fusilli", "penne",
    "tagliatelle", "macaroni", "lasagne", "dip", "houmous",
    "ready meal", "sausage", "crumble", "pizza", "sandwich", "soup",
]


def has_word(name, words):
    return any(re.search(rf"\b{re.escape(w)}\b", name) for w in words)

def strip_accents(s):
    return "".join(c for c in unicodedata.normalize("NFKD", s) if not unicodedata.combining(c))

def is_dairy(name):
    n = strip_accents(name).lower()
    if has_word(n, NOT_DAIRY_WORDS):
        return False
    return has_word(n, DAIRY_WORDS)