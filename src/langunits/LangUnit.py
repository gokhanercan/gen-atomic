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
class LangUnitMeta:
    name: str
    type: ABCMeta


@dataclass
class LangUnitInfo:
    name: str
    prompt_text: str  # This is default text. TODO: rename


@dataclass
class EvalRequest:
    generated: str
    correct_case: str
    unit: Unit
    lang_unit_info: LangUnitInfo


@dataclass
class EvalResponse:
    passed: bool


class LangUnit(ABC):

    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def run_test(self, eval_req: EvalRequest) -> EvalResponse:
        pass

    @abstractmethod
    def prompt_text(self):
        pass

    @abstractmethod
    def get_unit_type(self) -> UnitType:
        pass

    def name(self) -> str:
        return self.__class__.__name__

    def create_info(self):
        return LangUnitInfo(self.name(), self.prompt_text())

    def __str__(self) -> str:
        return f"LU[{self.name()}]"

    def __repr__(self) -> str:
        return self.__str__()
