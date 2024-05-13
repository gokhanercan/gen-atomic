from abc import ABC, abstractmethod
from typing import List


class ModelProviderBase(ABC):
    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def ProviderName(self):
        pass

    @abstractmethod
    def ProviderName(self):
        pass

    @abstractmethod
    def Generate(self, description: str) -> str:
        pass

    @abstractmethod
    def ModelConfigurations(self)->List[str]:       #?? Model?
        pass
