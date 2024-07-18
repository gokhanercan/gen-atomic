from typing import List

from langunits.LangUnitFactory import LangUnitFactory


class API(object):
    """
    Facade API layer for easily interacting with the library.
    """
    def __init__(self) -> None:
        super().__init__()

    def GetLangUnitPluginNames(self)-> List[str]:
        names:str = [key for key in LangUnitFactory().Meta.keys()]
        return names

if __name__ == '__main__':
    print(API().GetLangUnitPluginNames())