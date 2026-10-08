# TODO: test rounding, missing data, weird formats

from database.normalize import normalize_price
from database.normalize import normalize_unit_price

def test_basic():
    assert normalize_price("£1.00", "100g") == 1.0

def test_double_weight():
    assert normalize_price("£2.00", "200g") == 1.0

def test_weird_spacing():
    assert normalize_price(" £1.50 ", " 150g ") == 1.0

def test_rounding():
    assert normalize_price("£1.49", "200g") == 0.745

def test_zero_weight():
    assert normalize_price("£1.00", "0g") == None

def test_pence_price():
    assert normalize_price("50p", "100g") == 0.5

def test_mg_weight():
    assert normalize_price("£1.00", "1000mg") == 100.0

def test_kg_weight():
    assert normalize_price("£1.00", "1kg") == 0.1

def test_unit_price_100g_format():
    assert normalize_unit_price("£0.82/100g") == 0.82

def test_unit_price_kg_format():
    assert normalize_unit_price("£8.20/kg") == 0.82

def test_unit_price_unknown_format():
    assert normalize_unit_price("£0.82/unknown") == None