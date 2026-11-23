from pathlib import Path
import pandas as pd
import sqlite3
from rapidfuzz import process, fuzz
import re


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


def clean(name):
    n = name.lower()
    for w in ["sainsbury's", "stamford street co." "tesco", "british"]:
        n = n.replace(w, "")
    n = re.sub(r"\d+(\.\d+)?\s*(g|kg|ml|l|litre|pack|pints?)\b", "", n)
    return " ".join(n.split())


def df_split(df):
    tesco = df[df["store"] == "Tesco"]
    sainsburys = df[df["store"] == "Sainsburys"]

    tesco_products = tesco["product"].tolist()
    sainsburys_products = sainsburys["product"].tolist()
    return tesco_products, sainsburys_products


def match_products():
    df = load_latest()
    df["clean"] = df["product"].apply(clean)

    tesco = df[df["store"] == "Tesco"]
    sains = df[df["store"] == "Sainsburys"]

    matches = []

    for _, t in tesco.iterrows():
        pool = sains[sains["unit_type"] == t["unit_type"]]
        if pool.empty:
            continue
        match = process.extractOne(
            t["clean"],
            pool["clean"].tolist(),
            scorer=fuzz.token_sort_ratio,
            score_cutoff=70,
        )
        if match:
            s = pool.iloc[match[2]]
            matches.append((t, s, match[1]))

    return matches


def write_matches(matches):
    output = Path("compared.txt")
    with output.open("w", encoding="utf-8") as file:
        file.write(
            "Closest product candidates (fuzzy matches; not manually verified)\n"
        )
        file.write(
            "Tesco product | Sainsbury's candidate | Tesco unit | Sainsbury's unit | cheaper | match quality score (/100)\n"
        )
        for t, s, score in matches:
            if t["unit_value"] == s["unit_value"]:
                cheaper = "same"
            elif t["unit_value"] < s["unit_value"]:
                cheaper = "Tesco"
            else:
                cheaper = "Sainsburys"
            file.write(
                f"{t['product']} | {s['product']} | "
                f"{t['unit_value']} | {s['unit_value']} | {cheaper} | "
                f"{score:.1f}\n"
            )
    return output


if __name__ == "__main__":
    matches = match_products()
    output = write_matches(matches)
    print(f"Wrote {len(matches)} product candidates to {output}")
