from enum import unique, Enum
from typing import List


class Dataset(object):
    def __init__(self):
        super().__init__()
        self.Units: List[Unit] = []


@unique
class UnitType(Enum):
    RegexVal = 0  # RegexValidators


class Unit(object):     #TODO: Find a better name for this. Field,Column,Case etc.

    def __init__(self, name: str, desc: str, unitType: UnitType, correctCases=None, incorrectCases=None):
        self.Name = name
        self.Description = desc
        self.UnitType: UnitType = unitType
        #Cases
        self.CorrectCases:List[str] = correctCases  # TODO: Is this ds generalizable to other langs?     #TODO: We need additonal and optional case desc for this, for defining specific cases.
        if(self.CorrectCases is None): self.CorrectCases = []
        self.IncorrectCases:List[str] = incorrectCases
        if (self.IncorrectCases is None): self.IncorrectCases = []

    @property
    def TotalCases(self):
        return len(self.CorrectCases) + len(self.IncorrectCases)

    def __str__(self) -> str:
        return f"{self.Name} ({self.TotalCases}) Cases"

    def __repr__(self) -> str:
        return f"{self.Name} ({self.TotalCases}) Cases"

