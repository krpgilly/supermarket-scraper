from database.filters import is_dairy

def test_eggs_in():
    assert is_dairy("Sainsbury's British Free Range Eggs Large x12")

def test_cheddar_in():
    assert is_dairy("Sainsbury's British Mature Cheddar Cheese 400g")

def test_tagliatelle_out():
    assert not is_dairy("Sainsbury's Fresh Egg Tagliatelle 250g")

def test_quiche_out():
    assert not is_dairy("Sainsbury's Cheese & Onion Quiche 400g")

def test_custard_tart_out():
    assert not is_dairy("Sainsbury's Egg Custard Tarts 4 x 81g")