from data.Dataset import UnitType
from units.RegexVal.RegexVal import RegexVal
from units.UnitBase import UnitBase


class UnitFactory(object):

    def __init__(self) -> None:
        super().__init__()

    def Create(self,unitType:UnitType)->UnitBase:
        units:UnitBase = None

        #Unit Selection
        if unitType == UnitType.RegexVal:
            unit = RegexVal(unitType)
        else:
            raise Exception(f"No provider found for the type '{self}'")

        return unit
