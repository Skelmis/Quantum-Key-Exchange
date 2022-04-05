import random
from typing import Literal


class Qubit:
    def __init__(self, value: int, polarization: Literal[0, 1]):
        self.value: int = value
        self.polarization: Literal[0, 1] = polarization

    @property
    def is_circular_polarization(self) -> bool:
        return self.polarization == 0

    @property
    def is_linear_polarization(self) -> bool:
        return self.polarization == 1

    @classmethod
    def new(cls, value: int, polarization: Literal[0, 1]) -> "Qubit":
        return cls(value, polarization)

    def set(self, value: int, polarization: Literal[0, 1]) -> "Qubit":
        self.value = value
        self.polarization = polarization
        return self

    def measure(self, polarization: Literal[0, 1]) -> int:
        """
        Returns the value if polarizations match,
        otherwise we set the polarization to the new polarization
        and randomly set self.value to a 0 or 1

        Returns
        -------
        int
            The value
        """
        if polarization != self.polarization:
            value = random.choice((0, 1))
            self.set(value, polarization)

        return self.value
