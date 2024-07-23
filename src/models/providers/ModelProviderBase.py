from abc import ABC, abstractmethod
from typing import List
from data.Dataset import *
from langunits.LangUnitFactory import LangUnitInfo
from models.ModelBase import ModelBase


class ModelProviderBase(ModelBase):
    def __init__(self) -> None:
        super().__init__()

    # @abstractmethod
    # def ProviderName(self):
    #     pass
    #
    # @abstractmethod
    # def ProviderAbbreviation(self):
    #     pass

    @abstractmethod
    def ModelConfigurations(self)->List[str]:          #?Keys or Names ??
        pass