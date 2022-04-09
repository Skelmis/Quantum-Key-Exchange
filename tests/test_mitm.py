from assignment_2 import Client, Server, MITM


def test_init(client: Client, server: Server):
    original_establish_connection = server.establish_connection
    assert original_establish_connection == server.establish_connection

    mitm: MITM = MITM(client, server)
    assert mitm._client == client
    assert mitm._server == server
    assert original_establish_connection != server.establish_connection
    assert server.establish_connection == mitm.injected_establish_connection
