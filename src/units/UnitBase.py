from abc import ABC, abstractmethod

from data.Dataset import UnitType


class UnitBase(ABC):

    def __init__(self, unitType:UnitType) -> None:
        super().__init__()
        self.UnitType:UnitType = unitType

    # def CheckSyntax(self, code: str):
    #     """Implement any syntax checker if it has any"""
    #     pass

    #@abstractmethod
    # def Execute(self, code: str):
    #     pass

    # @abstractmethod
    def RunTest(self, code:str, correctCase:str)->bool:       #TODO: add more test oracle types here. Currently bool for RegexVal
        """Run the unit with test data"""
        pass