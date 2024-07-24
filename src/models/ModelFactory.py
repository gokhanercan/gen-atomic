from models.ModelBase import *
from models.providers.ModelProviderBase import ModelProviderBase
from utility import Discovery
from utility.PrintHelper import Print

class ModelFactory(object):
    def __init__(self) -> None:
        super().__init__()
        self.StandaloneModelsMeta:dict[str, StandaloneModelMeta] = self._DiscoverStandaloneModels() #Name|Meta
        self.ModelProvidersMeta: dict[str, ModelProviderMeta] = self._DiscoverModelProviders()      #Name|Meta
        #Model Auto Key Indexing via instances
        self.ModelIndex:dict[str:ModelMeta] = self._BuildModelIndex()                               #Key|Meta

    def _BuildModelIndex(self)->dict[str:ModelMeta]:
        index: dict[str:ModelMeta] = {}

        #Standalones
        for k,v in self.StandaloneModelsMeta.items():
            sMeta:StandaloneModelMeta = v
            sModel:ModelBase = self.CreateModel(sMeta.Name)
            key:str = sModel.Key()
            meta:ModelMeta = ModelMeta(Name=sMeta.Name,PlainName=sModel.PlainName(),Key=key,StandaloneModelMeta=sMeta, ModelProviderMeta = None)
            index[key] = meta
            sModel.ModelMeta = meta

        #Provider Models
        for k, v in self.ModelProvidersMeta.items():
            mpMeta: ModelProviderMeta = v
            models: List[ModelBase] = self.CreateModelsByProvider(mpMeta.Name)
            for m in models:
                key:str = m.Key()
                meta:ModelMeta = ModelMeta(Name=m.Name(),PlainName=m.PlainName(),Key=key,StandaloneModelMeta=None,ModelProviderMeta=mpMeta)
                index[key] = meta
                m.ModelMeta = meta
        return index

    #region Model Instance Creators
    def CreateModelByKey(self, key:str)->ModelBase:
        meta:ModelMeta = self.ModelIndex[key]
        if(meta.IsStandalone):
            m: ModelBase = self.CreateModel(meta.Name)
            return m
        else:
            mp:ModelProviderBase = self.CreateModelProvider(meta.ModelProviderMeta.Name, meta.PlainName)
            return mp
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
    def CreateModelProvider(self, providerName:str, modelName:Optional[str] = None)->ModelProviderBase:
        t:ABCMeta = self.ModelProvidersMeta[providerName].Type
        mp:ModelProviderBase = t.__new__(t)
        mp.__init__(modelName)
        return mp
    def CreateModelsByProvider(self, providerName:str)->List[ModelProviderBase]:
        p:ModelProviderBase = self.CreateModelProvider(providerName)
        modelNames = p.ModelNames()
        mps:List[ModelProviderBase] = []
        for modelName in modelNames:
            mp:ModelProviderBase = self.CreateModelProvider(providerName,modelName)
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
    def GetAllModelKeys(self)->List[str]:       #TODO: add some filters here. ExcludeBaselines, FilterByModelName, ByProviderName etc.
        return [k for k,v in self.ModelIndex.items()]

    #endregion

    # region Discovery
    @staticmethod
    def _DiscoverBaselineModels() -> dict[str, StandaloneModelMeta]:
        """
        Lists all available baseline model names
        :return:
        """
        return {k: v for k, v in ModelFactory._DiscoverStandaloneModels().items() if v.IsBaseline}

    @staticmethod
    def _DiscoverStandaloneModels() -> dict[str, StandaloneModelMeta]:
        """
        Discovers standalone models, not server through model providers
        :return:
        """
        types = Discovery.find_subclasses("models",ModelBase)  # TODO: It can be in any module when it is a plugin. Remove that criteria
        metas: dict[str, StandaloneModelMeta] = {}
        for t in types:
            name: str = t.__name__
            isBaseline: bool = issubclass(t, BaselineModel)
            if issubclass(t, ModelProviderBase):
                continue  # Skipping non-standalone models here. They are discovered in a separate process
            meta = StandaloneModelMeta(name, t, isBaseline)
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
    #STATIC Discovery
    Print("BaselineModelsMeta",     ModelFactory._DiscoverBaselineModels())
    Print("StandaloneModelsMeta",   ModelFactory._DiscoverStandaloneModels())
    Print("ModelProvidersMeta",     ModelFactory._DiscoverModelProviders())

    #INSTANCE Queries
    factory = ModelFactory()
    Print("ModelProviderNames",   factory.GetAllModelProviderNames())
    Print("StandaloneModelNames", factory.GetAllStandaloneModelNames())
    Print("BaselineModelNames",   factory.GetAllBaselineModelNames())

    #Keys
    Print("ModelIndex", factory.ModelIndex)
    Print("AllModelKeys",  factory.GetAllModelKeys())

    #Models Instance Creation
    Print("BaselineModels",   factory.CreateBaselineModels())
    Print("StandaloneModels", factory.CreateStandaloneModels())
    Print("ModelProviders",   factory.CreateModelProviders())
    #usages
    Print("CreateModel(name) usage", factory.CreateModel("RandomModel"))
    Print("CreateModelProvider(name) usage",factory.CreateModelProvider("OllamaModelProvider"))
    Print("CreateModelsByProvider(name) usage",factory.CreateModelsByProvider("OllamaModelProvider"))
    Print("CreateModelByKey(key) usage via standalones", factory.CreateModelByKey("np.random"))
    Print("CreateModelByKey(key) usage via providers", factory.CreateModelByKey("ol.codellama"))
















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