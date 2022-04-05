from assignment_2 import Qubit


def test_init():
    qubit: Qubit = Qubit(1, 1)

    assert qubit.value == 1
    assert qubit.polarization == 1
    assert qubit.is_linear_polarization
    assert not qubit.is_circular_polarization


def test_new():
    qubit: Qubit = Qubit.new(1, 1)

    assert isinstance(qubit, Qubit)
    assert qubit.value == 1
    assert qubit.polarization == 1
    assert qubit.is_linear_polarization
    assert not qubit.is_circular_polarization

    qubit_2: Qubit = qubit.new(1, 1)
    assert isinstance(qubit_2, Qubit)
    assert qubit == qubit_2
    assert id(qubit) != id(qubit_2)


def test_set():
    qubit: Qubit = Qubit(1, 1)
    assert qubit.value == 1
    assert qubit.polarization == 1
    assert qubit.is_linear_polarization
    assert not qubit.is_circular_polarization

    qubit.set(5, 0)
    assert qubit.value == 5
    assert qubit.polarization == 0
    assert qubit.is_circular_polarization
    assert not qubit.is_linear_polarization


def test_measure__same():
    """Tests Qubit measurement with the same polarizations."""
    qubit: Qubit = Qubit(5, 1)
    assert qubit.measure(1) == 5

    qubit_2: Qubit = Qubit(1, 0)
    assert qubit_2.measure(0) == 1


def test_measure__different():
    """Tests Qubit measurement with different polarizations"""
    # Given its random, we just test what we can
    qubit: Qubit = Qubit(5, 1)
    r_1: int = qubit.measure(0)
    assert isinstance(r_1, int)
    assert qubit.polarization == 0
    assert r_1 in (0, 1)

    qubit_2: Qubit = Qubit(1, 0)
    r_2: int = qubit_2.measure(1)
    assert isinstance(r_2, int)
    assert qubit_2.polarization == 1
    assert r_2 in (0, 1)
