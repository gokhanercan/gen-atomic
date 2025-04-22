from abc import ABC, abstractmethod
from data.Dataset import *
from models.ModelBase import ModelBase, ModelInfo
from utility import StringHelper


class ModelProviderBase(ModelBase):
    def __init__(self, activeModelName:str = None) -> None:
        super().__init__()
        self.ActiveModelName:Optional[str] = activeModelName
    def ModelName(self)->str:
        return self.ActiveModelName if(not StringHelper.IsNullOrEmpty(self.ActiveModelName)) else self.ProviderName()
    def Name(self) ->str:
        return self.ModelName()

    @abstractmethod
    def ModelNames(self)->List[str]:       #str:ModelNames
        pass
    def GetModelConf(self)->ModelInfo:      #TODO: rename this cause we will have a ModelConfiguration class.
        return ModelInfo(self.ModelName(), self.ProviderName(), self.ProviderAbbreviation())