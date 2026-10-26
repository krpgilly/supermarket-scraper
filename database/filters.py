import re

DAIRY_WORDS = [
    "milk", "cheese", "cheddar", "butter", "yogurt", "yoghurt",
    "eggs", "brie", "mozzarella", "feta", "halloumi",
    "parmesan", "parmigiano",
]

NOT_DAIRY_WORDS = [
    "tart", "tarts", "quiche", "pasty", "pastry", "pie", "pies",
    "baguette", "tortelloni", "ravioli", "pasta", "fusilli", "penne",
    "tagliatelle", "macaroni", "lasagne", "dip", "houmous",
    "ready meal", "sausage", "crumble", "pizza", "sandwich", "soup",
]


def has_word(name, words):
    return any(re.search(rf"\b{re.escape(w)}\b", name) for w in words)


def is_dairy(name):
    n = name.lower()
    if has_word(n, NOT_DAIRY_WORDS):
        return False
    return has_word(n, DAIRY_WORDS)