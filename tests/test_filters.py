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

def test_double_cream_in():
    assert is_dairy("Sainsbury's Double Cream 300ml")

def test_buttersoft_in():
    assert is_dairy("Sainsbury's Buttersoft Spreadable 500g")

def test_dairy_drink_in():
    assert is_dairy("Sainsbury's Everyday Lactose Free Semi Skimmed Dairy Drink 1L")

def test_soured_cream_dip_out():
    assert not is_dairy("Sainsbury's Soured Cream & Chive Dip 200g")

def test_soya_drink_out():
    assert not is_dairy("Sainsbury's Unsweetened Soya Drink 1L")

def test_creme_fraiche_in():
    assert is_dairy("Sainsbury's British Crème Fraîche 300ml")