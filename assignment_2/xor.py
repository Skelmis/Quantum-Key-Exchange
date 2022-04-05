from typing import Set


class XOR:
    """An XOR based cipher which works
    based off strings for simplicity.
    """

    def __init__(self, key: str):
        self.__assert_correct_format(key)
        self.__key: str = key

    def set_key(self, key: str) -> None:
        """Change the XOR key"""
        self.__assert_correct_format(key)
        self.__key = key

    @staticmethod
    def __assert_correct_format(entry: str) -> None:
        """
        Asserts the provided entry meets the
        requirements for XOR'ing.
        I.e. it is only 1's or 0's

        Parameters
        ----------
        entry: str
            The string we wish to check

        Raises
        ------
        ValueError
            The provided entry does
            not meet the required format
        """
        if not isinstance(entry, str):
            raise ValueError(f"Expected str found {entry.__class__.__name__}")

        _valid_lookups: Set[str] = {"0", "1", " "}  # Pre-computed fun
        for char in entry:
            if char not in _valid_lookups:
                raise ValueError(f"Expected only 1's or 0's or spaces, found {char}")

    def __key_to_length(self, required_length: int) -> str:
        """
        Generate the required XOR key.

        Parameters
        ----------
        required_length: int
            The length of the message we need
            to XOR against, this sets the
            required length of our key.

        Returns
        -------
        str
            The key repeated to the required length
        """
        # Adapted from:
        # https://stackoverflow.com/a/3391106/13781503
        current_key_length: int = len(self.__key)
        repetitions, extra = divmod(required_length, current_key_length)
        return self.__key * repetitions + self.__key[:extra]

    def __xor_message(self, message: str) -> str:
        # Frankly, disgusting.
        self.__assert_correct_format(message)
        key: str = self.__key_to_length(len(message))

        output = ""

        for i, char in enumerate(message):
            if (char == "1" and key[i] == "1") or (char == "0" and key[i] == "0"):
                output += "0"

            elif char == " ":
                output += " "

            else:
                output += "1"

        return output

    def decode(self, message: str) -> str:
        """
        Decipher a given message back
        to its original state.

        Parameters
        ----------
        message: str
            The message to decode

        Returns
        -------
        str
            The decoded message
        """
        return self.__xor_message(message)

    def encode(self, message: str) -> str:
        """
        Given a message, encode it
        via XOR with our stored key.

        Parameters
        ----------
        message: str
            The message to encode

        Returns
        -------
        str
            The encoded message
        """
        return self.__xor_message(message)
