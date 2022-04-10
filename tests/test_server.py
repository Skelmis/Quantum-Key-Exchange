import typing
import pytest

from assignment_2 import Server, Client


# noinspection PyUnresolvedReferences
@pytest.mark.parametrize(
    "stream_length",
    [16, 256, 1024],
)
def test_establish_connection(stream_length, client: Client, server: Server):
    # this also inherently tests `Server.finalize_key_with_client`
    # is working as expected. So two for 1
    assert client._server is None
    assert server._client is None
    assert len(server._Server__qubit_stream) == 0

    server.establish_connection(client, stream_length)

    assert client._server is not None
    assert server._client is not None
    assert client._server == server
    assert server._client == client
    assert client._Client__has_established_key is True
    assert client._Client__xor is not None
    assert server._Server__xor is not None
    assert len(server._Server__qubit_stream) != 0


@pytest.mark.parametrize(
    "stream_length",
    [16, 256, 1024],
)
def test_send(stream_length, client: Client, server: Server):
    server.establish_connection(client, stream_length)

    assert client.pending_message_amount == 0
    server.send("hello")
    assert client.pending_message_amount == 1
    server.send("01110111 01101111 01110010 01101100 01100100", is_already_binary=True)
    assert client.pending_message_amount == 2

    assert client.read() == "hello"
    assert client.read() == "world"

    assert client.pending_message_amount == 0
    server.send("Foo bar!")
    assert client.pending_message_amount == 1
    assert client.read() == "Foo bar!"
    assert client.pending_message_amount == 0


@pytest.mark.parametrize(
    "stream_length",
    [16, 256, 1024],
)
def test_invalid_send(stream_length, client: Client, server: Server):
    with pytest.raises(RuntimeError):
        server.send("Hello")
