from abc import ABC, abstractmethod
from typing import Optional

from deprecated import deprecated

from units.UnitBase import UnitBase
from utility import StringHelper


class ModelConf(object):
    def __init__(self, modelName:str, providerName:Optional[str] = None, providerAbbreviation:Optional[str] = None) -> None:
        super().__init__()
        self.ModelName:str = modelName
        self.ProviderName:Optional[str] = providerName
        self.ProviderAbbreviation: Optional[str] = providerAbbreviation

    def ConfigKey(self):
        abbr:str = StringHelper.Coelesce(self.ProviderAbbreviation,"np")
        return f"{abbr.lower()}-{self.ModelName.lower()}"

    def __str__(self) -> str:
        return self.ConfigKey()

    def __repr__(self) -> str:
        return self.ConfigKey()


class ModelBase(ABC):
    def __init__(self) -> None:
        super().__init__()

    def ModelName(self):        #TODO: delete
        return str(type(self).__name__).replace("Model","")

    #@abstractmethod
    def ProviderName(self)->str:
        return "NoProvider"

    def ProviderAbbreviation(self)->str:
        return "np"

    @deprecated
    def ModelConfAbbr(self)->str:       #TODO: DRY. Remove.
        #return f"{self.ProviderAbbreviation().lower()}-{self.ModelName().lower()}"
        return self.GetModelConf().ConfigKey()

    def ConfigKey(self):
        return self.GetModelConf().ConfigKey()

    def GetModelConf(self)->ModelConf:
        return ModelConf(self.ModelName(),self.ProviderName(),self.ProviderAbbreviation())

    @abstractmethod
    def Generate(self, description: str, unit: UnitBase) -> str:
        pass