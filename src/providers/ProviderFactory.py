from typing import List

from models.ModelBase import ModelBase
from providers.ChatGPTModelProvider import ChatGPTModelProvider
from providers.ModelProviderBase import ModelProviderBase
from providers.OllamaModelProvider import OllamaModelProvider


class ProviderFactory(object):

    def __init__(self) -> None:
        super().__init__()

    @staticmethod
    def GetAllProviderNames():
        """
        List of available provider names.
        :return:
        """
        return ["ollama","chatgpt"]     #TODO: Auto detect available ones.

    def CreateModelConfigurations(self, providerName:str)->List[ModelBase]:
        if(providerName == "ollama"):
            modelconfs:List[str] = OllamaModelProvider.ModelConfigurationsList()
            models:List[ModelBase] = []
            for modelconf in modelconfs:
                m:ModelBase = OllamaModelProvider(modelconf)
                models.append(m)
            return models

        if(providerName == "chatgpt"):
            modelconfs:List[str] = ChatGPTModelProvider.ModelConfigurationsList()
            models:List[ModelBase] = []
            for modelconf in modelconfs:
                m:ModelBase = ChatGPTModelProvider(modelconf)
                models.append(m)
            return models
        else:
            raise Exception(f"No model implementation found for '{providerName}'.")