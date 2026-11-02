from database.filters import has_word
import unicodedata

CATEGORY_RULES = [
    ("extra mature cheddar slices", ["extra mature cheddar slices", "extra mature cheddar cheese slices"]),
    ("extra mature grated cheddar", ["extra mature grated cheddar"]),
    ("extra mature cheddar", ["extra mature cheddar", "extra mature english cheddar"]),
    ("mature cheddar slices", ["mature cheddar slices", "mature cheddar cheese slices", "mature cheddar cheese 10 slices"]),
    ("mature grated cheddar", ["mature grated cheddar"]),
    ("mature cheddar", ["mature cheddar"]),
    ("mild cheddar", ["mild cheddar"]),
    ("medium cheddar", ["medium cheddar"]),
    ("salted butter", ["butter salted", "salted block butter", "salted butter"]),
    ("unsalted butter", ["butter unsalted", "unsalted butter"]),
    ("brie", ["brie"]),
    ("feta", ["feta"]),
    ("halloumi", ["halloumi"]),
    ("mozzarella", ["mozzarella"]),
    ("double cream", ["double cream"]),
    ("creme fraiche", ["creme fraiche"]),
    ("semi skimmed milk", ["semi skimmed milk", "semi skimmed longlife", "semi skimmed uht milk"]),
    ("skimmed milk", ["skimmed milk"]),
    ("whole milk", ["whole milk"]), ("medium cheddar slices", ["medium cheddar slices", "medium cheddar cheese slices"]),
    ("medium cheddar", ["medium cheddar"]),
]

def strip_accents(s):
    return "".join(c for c in unicodedata.normalize("NFKD", s) if not unicodedata.combining(c))


def categorise(name):
    n = strip_accents(name.lower()).replace("-", " ").replace(",", " ")
    n = " ".join(n.split())
    for category, words in CATEGORY_RULES:
        if has_word(n, words):
            return category
    return None