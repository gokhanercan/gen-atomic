from typing import Optional, List

from deprecated import deprecated

from models.ModelBase import ModelBase, ModelConf
from models.RandomModel import RandomModel
from models.StubModel import StubModel
from providers.ChatGPTModelProvider import ChatGPTModelProvider
from providers.OllamaModelProvider import OllamaModelProvider
from providers.ProviderFactory import ProviderFactory


class ModelFactory(object):

    def __init__(self) -> None:
        super().__init__()

    def GetModelNames(self)->[str]:           #TODO: GetModelNames and GetModelConfs, we need both!
        """
        Lists all available model names
        :return:
        """
        modelConfs:List[ModelConf] = self.GetModelConfigurations()
        modelNames:List[str] = []
        for modelConf in modelConfs:
            modelNames.append(modelConf.ModelName)

    def GetModelConfigurations(self)->[ModelConf]:
        modelConfs:[ModelConf] = []
        providerFactory = ProviderFactory()
        for providerName in ProviderFactory.GetAllProviderNames():
            modelConfigs:[ModelBase] = providerFactory.CreateModelConfigurations(providerName)
            for model in modelConfigs:
                modelConfs.append(model.GetModelConf())
        return modelConfs

    def ListFakeModelNames(self):
        """
        Lists all available fake model names
        :return:
        """
        return ["Stub","Random"]

    def CreateFakeModels(self)->[ModelBase]:
        models = []
        for modelName in self.ListFakeModelNames():
            m: ModelBase = self.CreateByCfg(ModelConf(modelName))
            models.append(m)
        return models

    def CreateAllModels(self)->[ModelBase]:
        """
        Creates instances of all available models.
        :return:
        """
        models = []
        for modelName in self.GetModelNames() + self.ListFakeModelNames():
            m: ModelBase = self.Create(modelName)
            models.append(m)
        return models

    def CreateByCfg(self, cfg:ModelConf)->ModelBase:
        if (cfg.ProviderName == "ollama"):
            return OllamaModelProvider(cfg.ModelName)
        if (cfg.ProviderName == "ollama"):
            return ChatGPTModelProvider(cfg.ModelName)
        if(cfg.ProviderName is None):
            if (cfg.ModelName == "Stub"):
                return StubModel()
            elif (cfg.ModelName == "Random"):
                return RandomModel()
        else:
            raise Exception(f"No model implementation found for '{cfg}'.")

    @deprecated
    def Create(self, providerName:str = Optional[str], modelConf:str = Optional[str])->ModelBase:
        if(not providerName and not modelConf): raise Exception("ProviderName or ModelName should be provided.")
        return self.Create(ModelConf(modelConf,providerName))