from abc import ABCMeta
from dataclasses import dataclass
from typing import List

from data.Dataset import UnitType
from units.RegexVal.RegexVal import RegexVal
from units.Sql.Sql import Sql
from units.UnitBase import UnitBase
from utility import Discovery


@dataclass
class UnitMeta(object):
    Name: str
    TypeError: ABCMeta


class UnitFactory(object):

    def __init__(self) -> None:
        super().__init__()
        self.Meta: dict[str, UnitMeta] = self.DiscoverUnits()

    def Create(self, unitType: UnitType) -> UnitBase:
        if unitType == UnitType.RegexVal:
            return RegexVal(unitType)
        if unitType == UnitType.SQLSelect:
            return Sql(unitType)
        else:
            raise Exception(f"No provider found for the type '{self}'")

    @staticmethod
    def DiscoverUnits() -> dict[str, UnitMeta]:  # Name | UnitMeta
        metas: dict[str, UnitMeta] = {}
        types: set = Discovery.find_subclasses("units", UnitBase)
        for type in types:
            name: str = type.__name__
            meta = UnitMeta(name, type)
            metas[name] = meta
        return metas


if __name__ == '__main__':
    unitFactory = UnitFactory().Meta
    print(unitFactory)
