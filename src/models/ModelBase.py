from abc import ABC, abstractmethod


class ModelBase(ABC):
    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def ModelName(self):
        pass

    @abstractmethod
    def Generate(self, description: str) -> str:  # desc: price for TK
        pass
