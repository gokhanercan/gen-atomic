from abc import ABC, abstractmethod
from data.Dataset import *
from models.ModelBase import ModelBase, ModelInfo
from utility import StringHelper


class ModelProviderBase(ModelBase):
    def __init__(self, active_model_name: str = None) -> None:
        super().__init__()
        self.active_model_name: Optional[str] = active_model_name

    def model_name(self) -> str:
        return self.active_model_name if (not StringHelper.IsNullOrEmpty(self.active_model_name)) else self.provider_name()

    def name(self) -> str:
        return self.model_name()

    @abstractmethod
    def model_names(self) -> list[str]:
        pass

    @deprecated("rename this cause we will have a ModelConfiguration class.")
    def get_model_conf(
        self,
    ) -> ModelInfo:
        return ModelInfo(self.model_name(), self.provider_name(), self.provider_abbreviation())
