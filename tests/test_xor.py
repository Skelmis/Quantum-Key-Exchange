import pytest

from assignment_2 import XOR


def test_init():
    xor: XOR = XOR("11111")
    assert xor._XOR__key == "11111"

    with pytest.raises(ValueError):
        XOR("hello world")


def test___assert_correct_format():
    """Tests that any provided data is either 1's or 0's"""
    XOR._XOR__assert_correct_format("000")
    XOR._XOR__assert_correct_format("111")
    XOR._XOR__assert_correct_format("0101")

    with pytest.raises(ValueError):
        XOR._XOR__assert_correct_format("010102")

    with pytest.raises(ValueError):
        XOR._XOR__assert_correct_format(10)


def test___key_to_length():
    """Tests we can receive the key which meets the length of input"""
    item = "hello world"
    key = XOR("1010")._XOR__key_to_length(len(item))
    assert len(key) == len(item)


def test_encode():
    xor: XOR = XOR("111")
    r_1: str = xor.encode("100")
    assert r_1 == "011"

    xor.set_key("101010")
    r_2: str = xor.encode("010101")
    assert r_2 == "111111"


def test_decode():
    xor: XOR = XOR("111")
    r_1: str = xor.decode("011")
    assert r_1 == "100"

    xor.set_key("101010")
    r_2: str = xor.decode("111111")
    assert r_2 == "010101"
