from queue import Queue
from typing import TYPE_CHECKING, Optional, List
from assignment_2 import Qubit, XOR
from assignment_2.util import (
    binary_string_to_string,
    gen_random,
    string_as_binary_string,
)

if TYPE_CHECKING:
    from assignment_2 import Client, Server


# noinspection DuplicatedCode
class MITM:
    """A man in the middle based attack vector.

    This utilises an attack vector more commonly
    known as ssl stripping, where the middle man
    acts like a client for the server, and a
    server for the real client.

    See the Client & Server for specific details.

    This doesn't use inheritance due to attribute
    sharing and the need to forward items.
    """

    def __init__(self, client: "Client", server: "Server"):
        self._client: "Client" = client
        self._server: "Server" = server

        # Client faking
        self.__has_established_key_with_server: bool = False
        self.__fake_client_xor: Optional[XOR] = None
        self.__hijacked_qubits: List[Qubit] = []
        self.__hijacked_received_qubits: List[Qubit] = []

        # Server faking
        self.__has_established_key_with_client: bool = False
        self.__qubit_stream: List[Qubit] = []
        self.__shared_qubits: List[Qubit] = []
        self.__fake_server_xor: Optional[XOR] = None

        # Also for queuing sends without the need
        # to immediately read
        self.__message_queue: Queue = Queue()

        # Lets hook ourself to the server, so
        # we can MITM without being detected
        self.__server_establish_connection = self._server.establish_connection
        self._server.establish_connection = self.injected_establish_connection

    def injected_establish_connection(self, _, stream_length: int = 16):
        self.__server_establish_connection(self, stream_length)  # type: ignore

    def set_server(self, server: "Server"):
        self._server = server

    def ingest_qubit(self, qubit: Qubit) -> None:
        if self.__has_established_key_with_server:
            raise RuntimeError

        self.__hijacked_received_qubits.append(
            Qubit.new(qubit.value, qubit.polarization)
        )

    def finalize_key_with_server(self) -> None:
        if self.__has_established_key_with_server:
            raise RuntimeError("Cannot re-establish a key with real server")

        self.__has_established_key_with_server = True

        polars: List[int] = []
        client_qubits: List[Qubit] = []
        for qubit in self.__hijacked_received_qubits:
            polar = gen_random()
            polars.append(polar)
            if polar == qubit.polarization:
                # We share polarization so we want to use this for our checks
                client_qubits.append(Qubit.new(qubit.measure(polar), polar))

        total_stream_length = len(self.__hijacked_received_qubits)
        self.establish_connection_as_fake_server(total_stream_length)

        self.__hijacked_qubits = client_qubits

        # Go tell the server what polarizations we used
        self._server.finalize_key_with_client(polars)

        # setup our xor
        key = "".join(str(i.value) for i in client_qubits)
        self.__fake_client_xor = XOR(key)

    def _raw_receive(self, message: str):
        self.__message_queue.put_nowait(message)

        raw_message = self.__fake_client_xor.decode(message)
        self.send(raw_message, is_already_binary=True)

    def read(self, *, as_binary: bool = False) -> str:
        raw_message = self.__fake_client_xor.decode(self.__message_queue.get_nowait())
        if not as_binary:
            raw_message = binary_string_to_string(raw_message)

        return raw_message

    @property
    def pending_message_amount(self) -> int:
        return self.__message_queue.qsize()

    def establish_connection_as_fake_server(self, stream_length: int = 16) -> None:
        self._client.set_server(self)  # type: ignore

        # Stream data qubits
        for i in range(stream_length):
            qubit: Qubit = Qubit(gen_random(), gen_random())
            self.__qubit_stream.append(qubit)

            self._client.ingest_qubit(qubit)

        self._client.finalize_key_with_server()

    def finalize_key_with_client(self, polarizations: List[int]) -> None:
        shared_qubits: List[Qubit] = []
        for i, polarization in enumerate(polarizations):
            if self.__qubit_stream[i].polarization == polarization:
                shared_qubits.append(self.__qubit_stream[i])

        self.__shared_qubits = shared_qubits

        # We should now have enough for a key
        key = "".join(str(i.value) for i in shared_qubits)
        self.__fake_server_xor = XOR(key)

    def send(self, message: str, *, is_already_binary: bool = False) -> None:
        if not is_already_binary:
            message = string_as_binary_string(message)

        encrypted_message = self.__fake_server_xor.encode(message)
        self._client._raw_receive(encrypted_message)
