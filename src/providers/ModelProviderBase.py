from abc import ABC, abstractmethod
from typing import List
from data.Dataset import *

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
    def ProviderAbbreviation(self):
        pass

    @abstractmethod
    def Generate(self, description: str, UnitType:UnitType) -> str:
        pass

    @abstractmethod
    def ModelConfigurations(self)->List[str]:       #?? Model?
        pass
