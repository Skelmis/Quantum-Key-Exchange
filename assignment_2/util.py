import random
from typing import Literal


def gen_random() -> Literal[0, 1]:
    return random.randint(0, 1)  # type: ignore


def string_as_binary_string(message: str) -> str:
    # https://stackoverflow.com/a/18815890/13781503
    return " ".join("{0:08b}".format(ord(x), "b") for x in message)


def binary_string_to_string(binary_string: str) -> str:
    # https://stackoverflow.com/a/40559005/13781503
    chunks = binary_string.split(" ")

    output = ""
    for item in chunks:
        output += chr(int(item, 2))
    return output
