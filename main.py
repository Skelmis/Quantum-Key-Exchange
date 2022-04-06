from typing import List

from assignment_2 import Client, Server, MITM


def main():
    client: Client = Client()
    server: Server = Server()
    mitm: MITM = MITM(client, server)

    # Discuss difference between ssl stripping and
    # actually eavesdropping the stream

    # defenses talk
    # look at tls auth process

    server.establish_connection(mitm)

    server.send("Hello world")
    server.send("This is a message from Ethan!")

    reads: List[str] = [client.read() for _ in range(client.pending_message_amount)]
    print("\n".join(reads))

    print("\nLets see if we middle manned this right?\n-----\n")
    mitm_reads: List[str] = [mitm.read() for _ in range(mitm.pending_message_amount)]
    print("\n".join(mitm_reads))


if __name__ == "__main__":
    main()
