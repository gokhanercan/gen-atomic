from abc import ABC, abstractmethod

from langunits.LangUnitFactory import LangUnitInfo
from utility import StringHelper
from data.Dataset import *

class BaselineModel(ABC):
    """
    This is a marker-type to indicate fake/stub/ummy baseline models.
    """
    pass

class ModelInfo(object):
    def __init__(self, plainName:str,
                       providerName:Optional[str] = None,
                       providerAbbreviation:Optional[str] = None) -> None:
        super().__init__()
        self.PlainName:str = plainName
        self.ProviderName:Optional[str] = providerName
        self.ProviderAbbreviation: Optional[str] = providerAbbreviation

    @deprecated()
    def ConfigKey(self)->str:
        abbr:str = StringHelper.Coelesce(self.ProviderAbbreviation,"np")
        return f"{abbr.lower()}.{self.PlainName.lower()}"
    def Key(self)->str:
        return self.ConfigKey()
    def __str__(self) -> str:
        return self.Key()
    def __repr__(self) -> str:
        return self.Key()

class ModelBase(ABC):
    def __init__(self) -> None:
        super().__init__()

    #region Names and Identities
    def Name(self)->str:
        return str(type(self).__name__)
    def PlainName(self)->str:
        return self.Name().replace("Model","").replace("Provider","")
    def ProviderName(self)->str:
        return "NoProvider"
    def ProviderAbbreviation(self)->str:
        return "np"
    @deprecated()
    def ConfigKey(self):
        return self.GetModelConf().ConfigKey()
    def Key(self):
        return self.GetModelConf().Key()
    def GetModelConf(self)->ModelInfo:
        return ModelInfo(self.PlainName(), self.ProviderName(), self.ProviderAbbreviation())
    # @deprecated
    # def ModelConfAbbr(self)->str:       #TODO: DRY. Remove.
    #     #return f"{self.ProviderAbbreviation().lower()}-{self.ModelName().lower()}"
    #     return self.GetModelConf().ConfigKey()
    #endregion

    @abstractmethod
    def Generate(self, description: str, langUnitInfo:LangUnitInfo) -> str:
        pass