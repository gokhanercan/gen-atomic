from abc import ABCMeta
from dataclasses import dataclass
from typing import List

from langunits.LangUnit import LangUnit
from utility import Discovery
from utility.PrintHelper import *


@dataclass
class LangUnitMeta(object):
    Name: str
    Type: ABCMeta

@dataclass
class LangUnitInfo(object):
    Name:str
    PromptText:str

class LangUnitFactory(object):

    def __init__(self) -> None:
        super().__init__()
        self.Meta: dict[str, LangUnitMeta] = self.DiscoverUnits()

    def CreateInfo(self, name:str):
        meta: LangUnitMeta = self.Meta[name]
        instance:LangUnit = self.Create(name)
        return LangUnitInfo(name,instance.PromptText())

    def Create(self, name:str)->LangUnit:
        meta:LangUnitMeta = self.Meta[name]
        t:ABCMeta = meta.Type
        instance:LangUnit = t.__new__(t)
        instance.__init__()
        return instance

    def GetAllLangUnitNames(self)-> List[str]:
        return [key for key in self.Meta.keys()]

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
    #Meta
    factory = LangUnitFactory()
    Print("LangUnitsMeta:", factory.Meta)

    #Instances
    sql:LangUnit = factory.Create("SqlSelect")
    Print("SqlSelect LangUnit", sql)
    Print("RegexVal LangUnit (Info)", factory.CreateInfo("RegexVal"))