import queue

import pytest

from assignment_2 import Client, Server, MITM, Qubit


def test_init(client: Client, server: Server):
    original_establish_connection = server.establish_connection
    assert original_establish_connection == server.establish_connection

    mitm: MITM = MITM(client, server)
    assert mitm._client == client
    assert mitm._server == server
    assert original_establish_connection != server.establish_connection
    assert server.establish_connection == mitm.injected_establish_connection


def test_set_server(client: Client, server: Server):
    mitm: MITM = MITM(client, server)
    assert mitm._server == server

    server_2: Server = Server()
    mitm.set_server(server_2)
    assert mitm._server != server
    assert mitm._server == server_2


def test_invalid_ingest_qubit(mitm: MITM):
    mitm._MITM__has_established_key_with_server = True

    with pytest.raises(RuntimeError):
        mitm.ingest_qubit(Qubit(1, 1))


# noinspection PyUnresolvedReferences
def test_ingest_qubit(mitm: MITM):
    assert len(mitm._MITM__hijacked_received_qubits) == 0
    mitm.ingest_qubit(Qubit(1, 1))
    assert len(mitm._MITM__hijacked_received_qubits) == 1


# noinspection PyUnresolvedReferences
@pytest.mark.parametrize(
    "stream_length",
    [16, 256, 1024],
)
def test_establish_connection(stream_length, mitm: MITM):
    client: Client = mitm._client
    server: Server = mitm._server
    assert client._server is None
    assert server._client is None
    assert mitm._MITM__fake_client_xor is None
    assert mitm._MITM__fake_server_xor is None

    server.establish_connection(client, stream_length)

    # Test that the real client and server are
    # actually talking to MITM, while we maintain
    # the correct connections
    assert mitm._client == client
    assert mitm._server == server
    assert client._server == mitm
    assert server._client == mitm
    assert mitm._MITM__fake_client_xor is not None
    assert mitm._MITM__fake_server_xor is not None


@pytest.mark.parametrize(
    "stream_length",
    [16, 256, 1024],
)
def test_raw_receive(stream_length, mitm: MITM):
    client: Client = mitm._client
    server: Server = mitm._server
    server.establish_connection(client, stream_length)

    assert mitm.pending_message_amount == 0
    assert client.pending_message_amount == 0
    server.send("Foo bar")

    assert mitm.pending_message_amount == 1
    assert client.pending_message_amount == 1

    assert mitm.read() == "Foo bar"
    assert client.read() == "Foo bar"

    assert mitm.pending_message_amount == 0
    assert client.pending_message_amount == 0
    server.send("01101000 01100101 01101100 01101100 01101111", is_already_binary=True)

    assert mitm.pending_message_amount == 1
    assert client.pending_message_amount == 1

    assert mitm.read() == "hello"
    assert client.read() == "hello"


@pytest.mark.parametrize(
    "stream_length",
    [16, 256, 1024],
)
def test_mitm_send(stream_length, mitm: MITM):
    client: Client = mitm._client
    server: Server = mitm._server
    server.establish_connection(client, stream_length)

    assert mitm.pending_message_amount == 0
    assert client.pending_message_amount == 0

    mitm.send("hello world")

    assert mitm.pending_message_amount == 0
    assert client.pending_message_amount == 1

    with pytest.raises(queue.Empty):
        mitm.read()

    assert client.read() == "hello world"
