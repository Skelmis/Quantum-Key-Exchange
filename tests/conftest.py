import random

import pytest

from assignment_2 import Client, Server, MITM


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


@pytest.fixture
def mitm(client: Client, server: Server):
    return MITM(client, server)
