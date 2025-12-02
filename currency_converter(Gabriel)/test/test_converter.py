from src.logic.converter import convert

def test_convert():
    assert convert(100, 1, 2) == 200
