from typing import List

from assignment_2 import Client, Server, MITM


def main():
    client: Client = Client()
    server: Server = Server()
    mitm: MITM = MITM(client, server)

    server.establish_connection(client)

    server.send("Hello world")
    server.send("This is a message from Ethan!")

    reads: List[str] = [client.read() for _ in range(client.pending_message_amount)]
    mitm_reads: List[str] = [mitm.read() for _ in range(mitm.pending_message_amount)]
    assert reads == mitm_reads
    print(reads)


if __name__ == "__main__":
    main()
