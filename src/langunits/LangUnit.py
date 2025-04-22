from abc import ABC, abstractmethod, ABCMeta
from enum import Enum
from dataclasses import dataclass
from data.Dataset import Unit


class UnitType(Enum):
    Expression = "Expression"
    Function = "Function"
    Class = "Class"
    Query = "Query"

@dataclass
class LangUnitMeta(object):
    Name: str
    Type: ABCMeta

@dataclass
class LangUnitInfo(object):
    Name:str
    PromptText:str      #This is default text. TODO: rename

class LangUnit(ABC):

    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def RunTest(self, code:str, correctCase:str, unit:Unit)->bool:
        pass

    @abstractmethod
    def PromptText(self):
        pass

    @abstractmethod
    def GetUnitType(self)->UnitType:
        pass

    def Name(self)->str:
        return self.__class__.__name__
    def CreateInfo(self):
        return LangUnitInfo(self.Name(),self.PromptText())
    def __str__(self) -> str:
        return f"LU[{self.Name()}]"
    def __repr__(self) -> str:
        return self.__str__()