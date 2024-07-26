from typing import List

from langunits.LangUnitFactory import LangUnitFactory
from models.ModelFactory import ModelFactory
from utility.PrintHelper import *


# noinspection PyMethodMayBeStatic
class API(object):
    """
    Facade API layer for easily interacting with the library.
    """
    def __init__(self) -> None:
        super().__init__()

    def GetAllLangUnitNames(self)-> List[str]:
        return LangUnitFactory().GetAllLangUnitNames()

    def GetAllModelProviderNames(self)-> List[str]:
        return ModelFactory().GetAllModelProviderNames()

    def GetAllModelKeys(self)-> List[str]:
        return ModelFactory().GetAllModelKeys()

if __name__ == '__main__':
    Print("LangUnits",      API().GetAllLangUnitNames())
    Print("ModelProviders", API().GetAllModelProviderNames())
    Print("ModelKeys",      API().GetAllModelKeys())