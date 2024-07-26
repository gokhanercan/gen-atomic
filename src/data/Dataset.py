from dataclasses import dataclass
from enum import unique, Enum
from typing import List, Optional

from pandas import DataFrame
from tabulate import tabulate
from deprecated import deprecated

class Dataset(object):
    def __init__(self, name:str):
        super().__init__()
        self.Units: List[Unit] = []
        self.Name = name

    def Print(self):
        ccCount:int = 0
        icCount:int = 0
        constraintCount:int = 0
        print(f"-- {self.Name.upper()} DATASET --")
        for u in self.Units:
            ccCount = ccCount + len(u.CorrectCases)
            icCount = icCount + len(u.IncorrectCases)
            constraintCount = constraintCount + len(u.Constraints)
        overall:int = ccCount + icCount + constraintCount
        df: DataFrame = DataFrame()
        df.at["Count",    "CorrectCase"] = str(ccCount)
        df.at["Count",    "IncorrectCase"] = str(icCount)
        df.at["Count",    "Overall"] = str(overall)
        df.at["Perc (%)", "CorrectCase"] = str(float(ccCount) / overall * 100)
        df.at["Perc (%)", "IncorrectCase"] = str(float(icCount) / overall * 100)
        df.at["Perc (%)", "Overall"] = str(100)
        print(tabulate(df, headers="keys", tablefmt='psql', floatfmt=".2f"))

@dataclass
class Criteria:
    name: str
    value: str

@dataclass
class Context:
    Data:str
    Schema:str

class Constraint(object):
    def __init__(self,criteria:Criteria):
        self.Criteria:Criteria = criteria

class Unit(object):     #TODO: Find a better name for this. Field,Column,Case etc.

    def __init__(self, name: str, desc: str, unitType: str, correctCases=None, incorrectCases=None):
        self.Name = name
        self.Description = desc
        self.UnitType: str = unitType

        self.Context: Optional[Context] = None
        self.Constraints: List[Constraint] = []

        #Cases
        self.CorrectCases:List[str] = correctCases  # TODO: Is this ds generalizable to other langs?     #TODO: We need additonal and optional case desc for this, for defining specific cases.
        if(self.CorrectCases is None): self.CorrectCases = []
        self.IncorrectCases:List[str] = incorrectCases
        if (self.IncorrectCases is None): self.IncorrectCases = []

    @property
    def TotalCases(self):
        return len(self.CorrectCases) + len(self.IncorrectCases)

    def __str__(self) -> str:
        return f"{self.Name} ({self.TotalCases} Cases)"

    def __repr__(self) -> str:
        return f"{self.Name} ({self.TotalCases} Cases)"

