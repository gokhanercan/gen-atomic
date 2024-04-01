from enum import unique, Enum
from typing import List

class Dataset(object):
    def __init__(self):
        super().__init__()

        self.Units:[Unit] = []

@unique
class UnitType(Enum):
    RegexVal = 0        #RegexValidators

class Unit(object):

    def __init__(self, name:str,desc:str,unitType:UnitType,
                 correctCases,incorrectCases):
        self.Name = name
        self.Description = desc
        self.CorrectCases:[str] = correctCases              #TODO: Is this ds generalizable to other langs?     #TODO: We need additonal and optional case desc for this, for defining specific cases.
        self.IncorrectCases:[str] = incorrectCases
        self.UnitType:UnitType = unitType

    def __str__(self) -> str:
        return  self.Name