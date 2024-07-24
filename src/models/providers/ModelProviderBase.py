from abc import ABC, abstractmethod
from data.Dataset import *
from models.ModelBase import ModelBase
from utility import StringHelper


class ModelProviderBase(ModelBase):
    def __init__(self, activeModelName:str = None) -> None:
        super().__init__()
        self.ActiveModelName:Optional[str] = activeModelName
    def ModelName(self)->str:
         return self.ActiveModelName if(not StringHelper.IsNullOrEmpty(self.ActiveModelName)) else "n/a"

    @abstractmethod
    def ModelNames(self)->List[str]:       #str:ModelNames
        pass