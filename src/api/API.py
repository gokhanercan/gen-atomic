from typing import List

from langunits.LangUnitFactory import LangUnitFactory
from models.ModelFactory import ModelFactory
from prompting.prompting_factory import PromptingFactory
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

    def get_all_prompting_keys(self) -> List[str]:
        return PromptingFactory().get_all_prompting_keys()


if __name__ == '__main__':
    Print("LangUnits",      API().GetAllLangUnitNames())
    Print("ModelProviders", API().GetAllModelProviderNames())
    Print("ModelKeys",      API().GetAllModelKeys())
    Print("PromptingKeys",  API().get_all_prompting_keys())