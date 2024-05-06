from abc import ABC, abstractmethod


class ModelBase(ABC):
    def __init__(self) -> None:
        super().__init__()


    def ModelName(self):
        return str(type(self).__name__).replace("Model","")

    @abstractmethod
    def Generate(self, description: str) -> str:  # desc: price for TK
        pass