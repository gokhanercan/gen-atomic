from enum import unique, Enum
from typing import List


class Dataset(object):
    def __init__(self):
        super().__init__()

        self.Units: [Unit] = []

    @staticmethod
    def SampleRegexValDataset():
        ds = Dataset()
        units = [
            Unit("Email", "email address", UnitType.RegexVal,
                 ["mail@gokhanercan.com", "amojtehed@gmail.com"],
                 ["dsadsadasda", "http://invalidaemail"]
                 ),
            Unit("PriceInTL", "price formatted with thousands seperator in Turkish Lira currency", UnitType.RegexVal,
                 ["1.550,5", "100"],
                 ["090", "0,23,34", "12.11,23", "aaaa", "mail@gokhan.com"]
                 )
        ]
        ds.Units = units
        return ds


@unique
class UnitType(Enum):
    RegexVal = 0  # RegexValidators


class Unit(object):

    def __init__(self, name: str, desc: str, unitType: UnitType,
                 correctCases, incorrectCases):
        self.Name = name
        self.Description = desc
        self.CorrectCases: [
            str] = correctCases  # TODO: Is this ds generalizable to other langs?     #TODO: We need additonal and optional case desc for this, for defining specific cases.
        self.IncorrectCases: [str] = incorrectCases
        self.UnitType: UnitType = unitType

    def __str__(self) -> str:
        return self.Name
