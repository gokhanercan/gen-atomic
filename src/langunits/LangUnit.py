from abc import ABC, abstractmethod
from enum import Enum

from data.Dataset import Unit

class UnitType(Enum):
    Expression = "Expression"
    Function = "Function"
    Class = "Class"
    Query = "Query"

class LangUnit(ABC):

    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def RunTest(self, code:str, correctCase:str, unit:Unit)->bool:
        pass

    @abstractmethod
    def PromptText(self):
        pass
    def Name(self)->str:
        return self.__class__.__name__
    @abstractmethod
    def GetUnitType(self)->UnitType:
        pass