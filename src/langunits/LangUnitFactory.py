from abc import ABCMeta
from dataclasses import dataclass
from langunits.LangUnit import LangUnit
from utility import Discovery


@dataclass
class LangUnitMeta(object):
    Name: str
    Type: ABCMeta

class LangUnitFactory(object):

    def __init__(self) -> None:
        super().__init__()
        self.Meta: dict[str, LangUnitMeta] = self.DiscoverUnits()

    # @deprecated()
    # def Create(self, unitType: UnitType) -> LangUnit:
    #     if unitType == UnitType.RegexVal:
    #         return RegexVal(unitType)
    #     if unitType == UnitType.SQLSelect:
    #         return Sql(unitType)
    #     else:
    #         raise Exception(f"No provider found for the type '{self}'")

    def CreateInstance(self, name:str)->LangUnit:
        meta:LangUnitMeta = self.Meta[name]
        t:ABCMeta = meta.Type
        instance:LangUnit = t.__new__(t)
        instance.__init__()
        return instance

    @staticmethod
    def DiscoverUnits() -> dict[str, LangUnitMeta]:  # Name | UnitMeta
        metas: dict[str, LangUnitMeta] = {}
        types:set = Discovery.find_subclasses("langunits", LangUnit)
        for type in types:
            name: str = type.__name__
            meta = LangUnitMeta(name, type)
            metas[name] = meta
        return metas


if __name__ == '__main__':
    factory = LangUnitFactory()
    print(factory.Meta)
    # sql:LangUnit = factory.CreateInstance("SqlSelect")
    # print(sql)
    # print(sql.PromptText())