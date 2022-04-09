import random

import pytest

from assignment_2 import Client, Server


@pytest.fixture(autouse=True)
def set_seed():
    """Sets the random seed for repeatable tests"""
    random.seed(12345654321)


@pytest.fixture
def client():
    return Client()


@pytest.fixture
def server():
    return Server()
