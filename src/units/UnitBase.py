from abc import ABC, abstractmethod

from data.Dataset import UnitType, Unit


class UnitBase(ABC):

    def __init__(self, unitType:UnitType) -> None:
        super().__init__()
        self.UnitType:UnitType = unitType

    # @abstractmethod
    def RunTest(self, code:str, correctCase:str, unit:Unit)->bool:
        pass