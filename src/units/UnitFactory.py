from data.Dataset import UnitType
from units.RegexVal.RegexVal import RegexVal
from units.UnitBase import UnitBase


class UnitFactory(object):

    def __init__(self) -> None:
        super().__init__()

    def Create(self,unitType:UnitType)->UnitBase:
        if unitType == UnitType.RegexVal:
            return RegexVal(unitType)
        else:
            raise Exception(f"No provider found for the type '{self}'")
