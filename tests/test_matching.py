import pandas as pd

from compare import match_products


def test_12_pack_matches_12_pack(monkeypatch):
    df = pd.DataFrame(
        [
            {
                "store": "Tesco",
                "product": "Tesco Large Free Range Eggs 12 Pack",
                "unit_type": "each",
            },
            {
                "store": "Sainsburys",
                "product": "Sainsbury's British Free Range Eggs Large x12",
                "unit_type": "each",
            },
            {
                "store": "Sainsburys",
                "product": "Sainsbury's British Free Range Eggs Large x6",
                "unit_type": "each",
            },
        ]
    )

    monkeypatch.setattr("compare.load_latest", lambda: df)

    matches = match_products()

    assert len(matches) == 1

    tesco, sains, score = matches[0]

    assert tesco["product"] == "Tesco Large Free Range Eggs 12 Pack"
    assert sains["product"] == "Sainsbury's British Free Range Eggs Large x12"
