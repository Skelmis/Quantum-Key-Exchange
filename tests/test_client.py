import queue
from queue import Empty
from typing import List

import pytest

from assignment_2 import Client, Server, Qubit, util, XOR


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
@pytest.mark.parametrize(
    "stream_length",
    [16, 256, 1024],
)
def test_valid_finalize_key_with_server(stream_length, client: Client, server: Server):
    assert client._Client__xor is None
    assert len(client._Client__client_qubits) == 0
    assert client._Client__has_established_key is False

    server.establish_connection(client, stream_length)
    assert client._Client__xor is not None
    assert len(client._Client__client_qubits) != 0
    assert client._Client__has_established_key is True


# noinspection PyUnresolvedReferences
@pytest.mark.parametrize(
    "stream_length",
    [16, 256, 1024],
)
def test_raw_receive(stream_length, client: Client, server: Server):
    assert client._Client__message_queue.empty()
    with pytest.raises(RuntimeError):
        client._raw_receive(util.string_as_binary_string("Hello"))

    server.establish_connection(client, stream_length)

    client._raw_receive(util.string_as_binary_string("Hello"))

    assert not client._Client__message_queue.empty()


# noinspection PyUnresolvedReferences,DuplicatedCode
@pytest.mark.parametrize(
    "stream_length",
    [16, 256, 1024],
)
def test_pending_message_amount(stream_length, client: Client, server: Server):
    assert client.pending_message_amount == 0

    server.establish_connection(client, stream_length)

    client._raw_receive(util.string_as_binary_string("Hello"))
    assert client.pending_message_amount == 1


def test_invalid_read(client: Client):
    with pytest.raises(RuntimeError):
        client.read()

    client._Client__xor = XOR("1010")
    client._Client__has_established_key = True

    with pytest.raises(Empty):
        client.read()


# noinspection PyUnresolvedReferences,DuplicatedCode
@pytest.mark.parametrize(
    "stream_length",
    [16, 256, 1024],
)
def test_read(stream_length, client: Client, server: Server):
    # setup
    server.establish_connection(client, stream_length)

    server.send("hello")
    server.send("world")

    assert client.read() == "hello"
    assert client.read(as_binary=True) == "01110111 01101111 01110010 01101100 01100100"

    with pytest.raises(queue.Empty):
        client.read()
