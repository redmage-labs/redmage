from redmage.convertors import BoolConvertor, StringConverter


def test_bool_convertor():
    convertor = BoolConvertor()
    assert convertor.convert("True")
    assert not convertor.convert("False")
    assert convertor.to_string(True) == "True"
    assert convertor.to_string(False) == "False"


def test_string_convertor():
    convertor = StringConverter()
    assert convertor.convert("test") == "test"
    assert convertor.convert("__empty__") == ""
    assert convertor.to_string("test") == "test"
    assert convertor.to_string("") == "__empty__"
