from typing import Optional, TYPE_CHECKING, List

from assignment_2 import Qubit, XOR
from assignment_2.util import gen_random, string_as_binary_string

if TYPE_CHECKING:  # pragma: no cover
    from assignment_2 import Client


class Server:
    def __init__(self):
        self._client: Optional["Client"] = None

        self.__xor: Optional[XOR] = None
        self.__qubit_stream: List[Qubit] = []
        self.__shared_qubits: List[Qubit] = []

    def establish_connection(self, client: "Client", stream_length: int = 16) -> None:
        self._client = client
        self._client.set_server(self)

        # Stream data qubits
        for i in range(stream_length):
            qubit: Qubit = Qubit(gen_random(), gen_random())
            self.__qubit_stream.append(qubit)

            self._client.ingest_qubit(qubit)

        self._client.finalize_key_with_server()

    def finalize_key_with_client(self, polarizations: List[int]) -> None:
        """
        Given the clients polarizations, figure out
        what the key should be using our local qubits.

        Parameters
        ----------
        polarizations: List[int]
            The clients Qubits
        """
        shared_qubits: List[Qubit] = []
        for i, polarization in enumerate(polarizations):
            if self.__qubit_stream[i].polarization == polarization:
                shared_qubits.append(self.__qubit_stream[i])

        self.__shared_qubits = shared_qubits

        # We should now have enough for a key
        key = "".join(str(i.value) for i in shared_qubits)
        self.__xor = XOR(key)

    def send(self, message: str, *, is_already_binary: bool = False) -> None:
        """Send an encrypted message to the client.

        Parameters
        ----------
        message: str
            The content to send
        is_already_binary: bool
            Whether or not the message is
            already a string of binary.

        Raises
        ------
        RuntimeError
            Client is not yet ready
            to receive messages.
        """
        if not self._client or not self.__shared_qubits:
            raise RuntimeError("Connection not yet established.")

        if not is_already_binary:
            message = string_as_binary_string(message)

        encrypted_message = self.__xor.encode(message)
        self._client._raw_receive(encrypted_message)
