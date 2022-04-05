from typing import List

from assignment_2 import Client, Server


def main():
    client: Client = Client()
    server: Server = Server()

    server.establish_connection(client)

    server.send("Hello world")
    server.send("This is a message from Ethan!")

    reads: List[str] = [client.read() for _ in range(client.pending_message_amount)]
    print("\n".join(reads))


if __name__ == "__main__":
    main()
