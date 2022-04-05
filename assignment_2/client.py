from queue import Queue
from typing import TYPE_CHECKING, Optional, List

from assignment_2 import Qubit, XOR
from assignment_2.util import gen_random, binary_string_to_string

if TYPE_CHECKING:
    from assignment_2 import Server


class Client:
    def __init__(self):
        self._server: Optional["Server"] = None
        self.__has_established_key: bool = False

        self.__xor: Optional[XOR] = None
        self.__client_qubits: List[Qubit] = []
        self.__received_qubits: List[Qubit] = []

        # Also for queuing sends without the need
        # to immediately read
        self.__message_queue: Queue = Queue()

    def set_server(self, server: "Server"):
        self._server = server

    def ingest_qubit(self, qubit: Qubit) -> None:
        """
        Receive a Qubit towards the key
        Parameters
        ----------
        qubit: Qubit
            The qubit to count towards the key

        Returns
        -------
        RuntimeError
            A key has already been established
        """
        if self.__has_established_key:
            raise RuntimeError

        self.__received_qubits.append(Qubit.new(qubit.value, qubit.polarization))

    def finalize_key(self) -> None:
        """Finalize the key and lock Qubit ingest."""
        if self.__has_established_key:
            raise RuntimeError("Cannot re-establish a key")

        self.__has_established_key = True

        polars: List[int] = []
        client_qubits: List[Qubit] = []
        for qubit in self.__received_qubits:
            polar = gen_random()
            polars.append(polar)
            if polar == qubit.polarization:
                # We share polarization so we want to use this for our checks
                client_qubits.append(Qubit.new(qubit.measure(polar), polar))

        self.__client_qubits = client_qubits

        # Go tell the server what polarizations we used
        self._server.finalize_key(polars)

        # setup our xor
        key = "".join(str(i.value) for i in client_qubits)
        self.__xor = XOR(key)

    def _raw_receive(self, message: str):
        """Used by the server to mock transports"""
        self.__message_queue.put_nowait(message)

    def read(self, *, as_binary: bool = False) -> str:
        """
        Read the next message from the server.

        Parameters
        ----------
        as_binary: bool
            Whether or not to return the
            message in binary or not.

            Defaults to False.

        Returns
        -------
        str
            The decoded message

        Raises
        ------
        Empty
            No pending messages
        """
        raw_message = self.__xor.decode(self.__message_queue.get_nowait())
        if not as_binary:
            raw_message = binary_string_to_string(raw_message)

        return raw_message

    @property
    def pending_message_amount(self) -> int:
        return self.__message_queue.qsize()
