from assignment_2 import util


def test_gen_random():
    # This uses seeded randomness in tests
    # to ensure a reproducible environment
    # Its also only 1 of 2 choices, so its
    # quite the mediocre test
    assert util.gen_random() == 1
    assert util.gen_random() == 0
    assert util.gen_random() == 1


def test_string_as_binary_string():
    assert (
        util.string_as_binary_string("hello world")
        == "01101000 01100101 01101100 01101100 01101111 "
        "00100000 01110111 01101111 01110010 01101100 01100100"
    )


def test_binary_string_to_string():
    assert (
        util.binary_string_to_string(
            "01101000 01100101 01101100 01101100 01101111 "
            "00100000 01110111 01101111 01110010 01101100 01100100"
        )
        == "hello world"
    )
