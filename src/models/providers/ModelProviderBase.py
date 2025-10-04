from abc import ABC, abstractmethod
from data.Dataset import *
from models.ModelBase import ModelBase, ModelInfo
from utility import StringHelper


class ModelProviderBase(ModelBase):
    def __init__(self, active_model_name: str = None) -> None:
        super().__init__()
        self.ActiveModelName: Optional[str] = active_model_name

    def ModelName(self) -> str:
        return self.ActiveModelName if (not StringHelper.IsNullOrEmpty(self.ActiveModelName)) else self.ProviderName()

    def Name(self) -> str:
        return self.ModelName()

    @abstractmethod
    def model_names(self) -> list[str]:
        pass

    @deprecated("rename this cause we will have a ModelConfiguration class.")
    def GetModelConf(
        self,
    ) -> ModelInfo:
        return ModelInfo(self.ModelName(), self.ProviderName(), self.ProviderAbbreviation())
