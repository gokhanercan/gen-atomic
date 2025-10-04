from dataclasses import dataclass
from enum import unique, Enum
from typing import List, Optional

from pandas import DataFrame
from tabulate import tabulate
from deprecated import deprecated


@dataclass
class Criteria:
    name: str
    value: str


@dataclass
class Context:
    data: str
    schema: str


class Constraint(object):
    def __init__(self, criteria: Criteria):
        self.criteria: Criteria = criteria


class Unit(object):  # TODO: Find a better name for this. Field,Column,Case etc.

    def __init__(
        self,
        name: str,
        desc: str,
        unit_type: str,
        correct_cases=None,
        incorrect_cases=None,
    ):
        self.name = name
        self.description = desc
        self.unit_type: str = unit_type

        self.context: Optional[Context] = None
        self.constraints: List[Constraint] = []

        # Cases
        self.correct_cases: List[str] = (
            correct_cases  # TODO: Is this ds generalizable to other langs?     #TODO: We need additional and optional case desc for this, for defining specific cases.
        )
        if self.correct_cases is None:
            self.correct_cases = []
        self.incorrect_cases: List[str] = incorrect_cases
        if self.incorrect_cases is None:
            self.incorrect_cases = []

    @property
    def total_cases(self):
        return len(self.correct_cases) + len(self.incorrect_cases)

    def __str__(self) -> str:
        return f"{self.name} ({self.total_cases} Cases)"

    def __repr__(self) -> str:
        return f"{self.name} ({self.total_cases} Cases)"


class Dataset(object):
    def __init__(self, name: str):
        super().__init__()
        self.units: List[Unit] = []
        self.name = name

    def print(self):
        cc_count: int = 0
        ic_count: int = 0
        constraint_count: int = 0
        print(f"-- {self.name.upper()} DATASET --")
        for u in self.units:
            cc_count = cc_count + len(u.correct_cases)
            ic_count = ic_count + len(u.incorrect_cases)
            constraint_count = constraint_count + len(u.constraints)
        overall: int = cc_count + ic_count + constraint_count
        df: DataFrame = DataFrame()
        df.at["Count", "CorrectCase"] = str(cc_count)
        df.at["Count", "IncorrectCase"] = str(ic_count)
        df.at["Count", "Overall"] = str(overall)
        df.at["Perc (%)", "CorrectCase"] = str(float(cc_count) / overall * 100)
        df.at["Perc (%)", "IncorrectCase"] = str(float(ic_count) / overall * 100)
        df.at["Perc (%)", "Overall"] = str(100)
        print(tabulate(df, headers="keys", tablefmt="psql", floatfmt=".2f"))
