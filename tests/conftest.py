import random

import pytest


@pytest.fixture(scope="session", autouse=True)
def set_seed():
    """Sets the random seed for repeatable tests"""
    random.seed(12345654321)
