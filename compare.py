from pathlib import Path
import pandas as pd
import sqlite3
from rapidfuzz import process, fuzz


def load_latest():
    conn = sqlite3.connect("products.db")
    df = pd.read_sql_query(
        """SELECT pr.id, s.name AS store, p.name AS product,
               pr.unit_value, pr.unit_type, pr.raw_price
        FROM prices pr
        JOIN products p ON pr.product_id = p.id
        JOIN stores s ON pr.store_id = s.id
""",
        conn,
    )

    conn.close()
    return df.sort_values("id").groupby(["store", "product"]).tail(1)


def df_split(df):
    tesco = df[df["store"] == "Tesco"]
    sainsburys = df[df["store"] == "Sainsburys"]

    tesco_products = tesco["product"].tolist()
    sainsburys_products = sainsburys["product"].tolist()
    return tesco_products, sainsburys_products


def match_products():
    df = load_latest()
    tesco_products, sainsburys_products = df_split(df)

    matches = []

    for product in tesco_products:
        match = process.extractOne(product, sainsburys_products, scorer=fuzz.WRatio)
        if match is not None and match[1] >= 62:
            matches.append((product, match[0], match[1], match[2]))

    return matches


def write_matches(matches):
    output = Path("compared.txt")
    with output.open("w", encoding="utf-8") as file:
        file.write(
            "Closest product candidates (fuzzy matches; not manually verified)\n"
        )
        file.write("Tesco product | Sainsbury's candidate | Similarity score\n")
        for tesco_product, sainsburys_product, score, index in matches:
            file.write(f"{tesco_product} | {sainsburys_product} | {score:.1f}\n")

    return output


matches = match_products()
output = write_matches(matches)
print(f"Wrote {len(matches)} product candidates to {output}")
