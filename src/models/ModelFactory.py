from abc import ABCMeta
from dataclasses import dataclass, field
from typing import Optional, List
from deprecated import deprecated
from models.ModelBase import *
from models.providers.ModelProviderBase import ModelProviderBase
from utility import Discovery

from utility.PrintHelper import Print


@dataclass
class ModelProviderMeta(object):
    Name: str
    Type: ABCMeta

@dataclass
class ModelMeta(object):
    Name: str
    Type: ABCMeta
    # ProviderName: Optional[str]
    IsBaseline: bool = field(default = False)

class ModelFactory(object):
    def __init__(self) -> None:
        super().__init__()
        self.StandaloneModelsMeta:dict[str, ModelMeta] = self._DiscoverStandaloneModels()
        self.ModelProvidersMeta: dict[str, ModelProviderMeta] = self._DiscoverModelProviders()

    # def GetModelKeys(self)->List[str]:           #TODO: GetModelNames and GetModelConfs, we need both!
    #     modelConfs:List[ModelConfInfo] = self.GetModelConfigurations()
    #     modelNames:List[str] = []
    #     for modelConf in modelConfs:
    #         modelNames.append(modelConf.ConfigKey())
    #     return modelNames

    # def GetModelConfigurations(self)->List[ModelConfInfo]:
    #     modelConfs:[ModelConfInfo] = []
    #     providerFactory = ModelFactory()
    #     for providerName in ModelFactory.GetAllModelProviderNames():
    #         modelConfigs:[ModelBase] = providerFactory.CreateModelConfigurations(providerName)
    #         for model in modelConfigs:
    #             modelConfs.append(model.GetModelConf())
    #     return modelConfs

    # def CreateAllModels(self)->[ModelBase]: #TODO:
    #     models = []
    #     for modelName in self.GetModelKeys() + self.ListFakeModelKeys():
    #         m: ModelBase = self.Create(modelName)
    #         models.append(m)
    #     return models

    # @deprecated("Just like what we did for ANTLR and LangUnit, we need a plugin-wise factory here to support open-closed principle.")
    # def CreateByCfg(self, cfg:ModelConfInfo)->ModelBase:
    #     if (cfg.ProviderName == "ollama"):
    #         return OllamaModelProvider(cfg.ModelName)
    #     if (cfg.ProviderName == "ollama"):
    #         return ChatGPTModelProvider(cfg.ModelName)
    #     if(cfg.ProviderName is None):
    #         if (cfg.ModelName == "Stub"):
    #             return StubModel()
    #         elif (cfg.ModelName == "Random"):
    #             return RandomModel()
    #     else:
    #         raise Exception(f"No model implementation found for '{cfg}'.")

    # @deprecated
    # def Create(self, providerName:str = Optional[str], modelConf:str = Optional[str])->ModelBase:
    #     if(not providerName and not modelConf): raise Exception("ProviderName or ModelName should be provided.")
    #     return self.CreateByCfg(ModelConfInfo(modelConf, providerName))

    #region Model Instance Creators
    def CreateAllModels(self):
        return self.CreateStandaloneModels() + self.CreateModelProviders()
    def CreateStandaloneModels(self)->List[ModelBase]:
        models:List[ModelBase] = []
        for modelName in self.GetAllStandaloneModelNames():
            m:ModelBase = self.CreateModel(modelName)
            models.append(m)
        return models
    def CreateBaselineModels(self)->List[ModelBase]:
        models:List[ModelBase] = []
        for modelName in self.GetAllBaselineModelNames():
            m:ModelBase = self.CreateModel(modelName)
            models.append(m)
        return models
    def CreateModelProviders(self)->List[ModelProviderBase]:
        providers:List[ModelProviderBase] = []
        for mpName in self.GetAllModelProviderNames():
            mp:ModelProviderBase = self.CreateModelProvider(mpName)
            providers.append(mp)
        return providers
    def CreateModelProvider(self, providerName:str, configName:Optional[str] = None)->ModelProviderBase:
        t:ABCMeta = self.ModelProvidersMeta[providerName].Type
        mp:ModelProviderBase = t.__new__(t)
        mp.__init__(configName)
        return mp
    def CreateModelsByProvider(self, providerName:str)->List[ModelProviderBase]:
        p:ModelProviderBase = self.CreateModelProvider(providerName)
        configNames = p.ModelConfigurations()
        mps:List[ModelProviderBase] = []
        for cfgName in configNames:
            mp:ModelProviderBase = self.CreateModelProvider(providerName,cfgName)
            mps.append(mp)
        return mps
    def CreateModel(self, modelName:str)->ModelBase:
        t:ABCMeta = self.StandaloneModelsMeta[modelName].Type
        m:ModelBase = t.__new__(t)
        m.__init__()
        return m
    #endregion

    #region Queries

    def GetAllModelProviderNames(self)->List[str]:
        return [k for k in self.ModelProvidersMeta]
    def GetAllStandaloneModelNames(self)->List[str]:
        return [k for k in self.StandaloneModelsMeta]
    def GetAllBaselineModelNames(self)->List[str]:
        return [key for key,value in self.StandaloneModelsMeta.items() if value.IsBaseline==True]       #Limited to standalone models only for now.
    def GetAllModelKeys(self, includeBaselines:bool = False)->List[str]:
        models = self.CreateAllModels()
        modelKeys = [m.Key() for m in models]
        return modelKeys

    #endregion
    # @deprecated()
    # def CreateModelConfigurations(self, providerName:str)->List[ModelBase]:
    #     if(providerName == "ollama"):
    #         modelconfs:List[str] = OllamaModelProvider.ModelConfigurationsList()
    #         models:List[ModelBase] = []
    #         for modelconf in modelconfs:
    #             m:ModelBase = OllamaModelProvider(modelconf)
    #             models.append(m)
    #         return models
    #
    #     if(providerName == "chatgpt"):
    #         modelconfs:List[str] = ChatGPTModelProvider.ModelConfigurationsList()
    #         models:List[ModelBase] = []
    #         for modelconf in modelconfs:
    #             m:ModelBase = ChatGPTModelProvider(modelconf)
    #             models.append(m)
    #         return models
    #     else:
    #         raise Exception(f"No model implementation found for '{providerName}'.")

    # region Discovery
    @staticmethod
    def _DiscoverBaselineModels() -> dict[str, ModelMeta]:
        """
        Lists all available baseline model names
        :return:
        """
        return {k: v for k, v in ModelFactory._DiscoverStandaloneModels().items() if v.IsBaseline}

    @staticmethod
    def _DiscoverStandaloneModels() -> dict[str, ModelMeta]:
        """
        Discovers standalone models, not server through model providers
        :return:
        """
        types = Discovery.find_subclasses("models",ModelBase)  # TODO: It can be in any module when it is a plugin. Remove that criteria
        metas: dict[str, ModelMeta] = {}
        for t in types:
            name: str = t.__name__
            isBaseline: bool = issubclass(t, BaselineModel)
            if issubclass(t, ModelProviderBase):
                continue  # Skipping non-standalone models here. They are discovered in a separate process
            meta = ModelMeta(name, t, isBaseline)
            metas[name] = meta
        return metas

    @staticmethod
    def _DiscoverModelProviders() -> dict[str, ModelProviderMeta]:
        types = Discovery.find_subclasses("models",ModelProviderBase,"providers")
        metas: dict[str, ModelProviderMeta] = {}
        for t in types:
            name: str = t.__name__
            meta = ModelProviderMeta(name, t)
            metas[name] = meta
        return metas
    # endregion

if __name__ == '__main__':
    #Static Discovery
    Print("BaselineModelsMeta",     ModelFactory._DiscoverBaselineModels())
    Print("StandaloneModelsMeta",   ModelFactory._DiscoverStandaloneModels())
    Print("ModelProvidersMeta",     ModelFactory._DiscoverModelProviders())

    #Instance Queries
    factory = ModelFactory()
    Print("ModelProviderNames",   factory.GetAllModelProviderNames())
    Print("StandaloneModelNames", factory.GetAllStandaloneModelNames())
    Print("BaselineModelNames",   factory.GetAllBaselineModelNames())
    #Keys
    Print("AllModelKeys",  factory.GetAllModelKeys())
    # print("Models:",[factory.CreateModelConfigurations(modelName) for modelName in factory.GetAllProviderNames()])

    #Models Instance Creation
    Print("BaselineModels",   factory.CreateBaselineModels())
    Print("StandaloneModels", factory.CreateStandaloneModels())
    Print("ModelProviders",   factory.CreateModelProviders())
    #usages
    Print("CreateModel(name) usage", factory.CreateModel("RandomModel"))        #typename or name or key ??
    Print("CreateModelProvider(name) usage",factory.CreateModelProvider("OllamaModelProvider"))
    Print("CreateModelsByProvider(name) usage",factory.CreateModelsByProvider("OllamaModelProvider"))
    #Models directly
    # ModelFactory().GetModelKeys()