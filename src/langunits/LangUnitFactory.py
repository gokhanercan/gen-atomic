from abc import ABCMeta
from typing import List

from langunits.LangUnit import LangUnit, LangUnitMeta
from utility import Discovery
from utility.PrintHelper import *


class LangUnitFactory(object):

    def __init__(self) -> None:
        super().__init__()
        self.meta: dict[str, LangUnitMeta] = self.discover_units()

    def create_info(self, name: str):
        instance: LangUnit = self.create(name)
        return instance.create_info()
        # meta: LangUnitMeta = self.meta[name]
        # instance:LangUnit = self.create(name)
        # return LangUnitInfo(name,instance.prompt_text())

    def create(self, name: str) -> LangUnit:
        meta: LangUnitMeta = self.meta.get(name)
        if meta is None:
            raise Exception(f"LangUnitFactory.create: Unknown LangUnit name '{name}'")
        t: ABCMeta = meta.type
        instance: LangUnit = t.__new__(t)
        instance.__init__()
        return instance

    def get_all_lang_unit_names(self) -> List[str]:
        return [key for key in self.meta.keys()]

    @staticmethod
    def discover_units() -> dict[str, LangUnitMeta]:  # Name | UnitMeta
        metas: dict[str, LangUnitMeta] = {}
        types: set = Discovery.find_subclasses("langunits", LangUnit)
        for type in types:
            name: str = type.__name__
            meta = LangUnitMeta(name, type)
            metas[name] = meta
        return metas


if __name__ == "__main__":
    # Meta
    factory = LangUnitFactory()
    Print("LangUnitsMeta:", factory.meta)

    # Instances
    sql: LangUnit = factory.create("SqlSelect")
    Print("SqlSelect LangUnit", sql)
    Print("RegexVal LangUnit (Info)", factory.create_info("RegexVal"))
