import pytest

from assignment_2 import Client, Server, Qubit


def test_set_server(client: Client, server: Server):
    assert client._server is None

    client.set_server(server)
    assert client._server is not None
    assert client._server is server


# noinspection PyUnresolvedReferences
def test_valid_ingest_qubit(client: Client):
    qubit: Qubit = Qubit(1, 1)

    assert client._Client__received_qubits == []
    assert len(client._Client__received_qubits) == 0

    client.ingest_qubit(qubit)
    assert len(client._Client__received_qubits) == 1
    assert client._Client__received_qubits == [qubit]


# noinspection PyUnresolvedReferences
def test_invalid_ingest_qubit(client: Client):
    client._Client__has_established_key = True

    with pytest.raises(RuntimeError):
        client.ingest_qubit(Qubit(1, 1))


# noinspection PyUnresolvedReferences
def test_invalid_finalize_key_with_server(client: Client):
    client._Client__has_established_key = True

    with pytest.raises(RuntimeError):
        client.finalize_key_with_server()


# noinspection PyUnresolvedReferences
def test_valid_finalize_key_with_server(client: Client, server: Server):
    assert client._Client__xor is None
    assert len(client._Client__client_qubits) == 0
    assert client._Client__has_established_key is False

    # Some test setup
    client.set_server(server)
    qubits: List[Qubit] = [Qubit(1, 1), Qubit(1, 0), Qubit(0, 1)]
    for q in qubits:
        client.ingest_qubit(q)
        server._Server__qubit_stream.append(q)

    client.finalize_key_with_server()
    assert client._Client__xor is not None
    assert len(client._Client__client_qubits) == 3
    assert client._Client__has_established_key is True


# def test_raw_receive(client: Client):
