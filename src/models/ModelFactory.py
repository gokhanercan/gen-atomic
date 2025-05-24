from models.ModelBase import *
from models.providers.ModelProviderBase import ModelProviderBase
from utility import Discovery
from utility.PrintHelper import Print

@dataclass
class ModelFilters:
    providerAbbr:str = None
    providerName:str = None
    keyContains:str = None
    isBaseline:Optional[bool] = None

class ModelFactory(object):
    def __init__(self) -> None:
        super().__init__()
        self.StandaloneModelsMeta:dict[str, StandaloneModelMeta] = self._DiscoverStandaloneModels() #Name|Meta
        self.ModelProvidersMeta: dict[str, ModelProviderMeta] = self._DiscoverModelProviders()      #Name|Meta
        #Model Auto Key Indexing via instances
        self.ModelIndex:dict[str,ModelMeta] = self._BuildModelIndex()                               #Key|Meta

    def _BuildModelIndex(self)->dict[str,ModelMeta]:
        index: dict[str:ModelMeta] = {}

        # Standalone ones
        for k,v in self.StandaloneModelsMeta.items():
            sMeta:StandaloneModelMeta = v
            sModel:ModelBase = self.CreateModel(sMeta.Name)
            key:str = sModel.Key()
            meta:ModelMeta = ModelMeta(Name=sMeta.Name,PlainName=sModel.PlainName(),Key=key,StandaloneModelMeta=sMeta, ModelProviderMeta = None)
            index[key] = meta
            sModel.ModelMeta = meta

        # Provider Models
        for k, v in self.ModelProvidersMeta.items():
            mpMeta: ModelProviderMeta = v
            models: List[ModelBase] = self.CreateModelsByProvider(mpMeta.Name)
            for m in models:
                key:str = m.Key()
                meta:ModelMeta = ModelMeta(Name=m.Name(),PlainName=m.PlainName(),Key=key,StandaloneModelMeta=None,ModelProviderMeta=mpMeta)
                index[key] = meta
                m.ModelMeta = meta
        return index

    # region Model Instance Creators
    def CreateModelByKey(self, key: str) -> ModelBase:
        meta:ModelMeta = self.ModelIndex[key]
        if(meta.IsStandalone):
            m: ModelBase = self.CreateModel(meta.Name,meta)
            return m
        else:
            mp:ModelProviderBase = self.CreateModelProvider(meta.ModelProviderMeta.Name, meta.PlainName)
            return mp

    def FindKeysByFilters(self,mf:ModelFilters):
        filtered:dict[str,ModelMeta] = self.ModelIndex
        # region Apply filters
        def filterProviderAbbr(filter:str,meta:ModelMeta):
            return filter == meta.Key.split('.')[0]
        def filterProviderName(filter:str,meta:ModelMeta):
            if(meta.ModelProviderMeta): return filter == meta.ModelProviderMeta.Name
            return False
        def filterKeyContains(filter:str,meta:ModelMeta):
            return meta.Key.__contains__(filter)
        # endregion

        if mf.providerAbbr:
            filtered = {k:v for k,v in filtered.items() if filterProviderAbbr(mf.providerAbbr,v)}
        if mf.providerName:
            filtered = {k: v for k, v in filtered.items() if filterProviderName(mf.providerName, v)}
        if mf.keyContains:
            filtered = {k: v for k, v in filtered.items() if filterKeyContains(mf.keyContains, v)}
        if mf.isBaseline:
            filtered = {k: v for k, v in filtered.items() if v.IsBaseline == mf.isBaseline}

        return filtered

    def CreateModelsByFilters(self, mf:ModelFilters)->List[ModelBase]:
        filtered:dict[str,ModelMeta] = self.FindKeysByFilters(mf)
        return [self.CreateModelByKey(k) for k,v in filtered.items()]

    def CreateAllModels(self)->List[ModelBase]:
        return [self.CreateModelByKey(k) for k,v in self.ModelIndex.items()]

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

    def CreateModel(self, modelName:str, modelMeta:ModelMeta | None = None)->ModelBase:
        t:ABCMeta = self.StandaloneModelsMeta[modelName].Type
        m:ModelBase = t.__new__(t)
        m.__init__()
        if(modelMeta): m.ModelMeta = modelMeta
        return m

    # endregion

    #region Queries

    def GetAllModelProviderNames(self)->List[str]:
        return [k for k in self.ModelProvidersMeta]
    def GetAllModelProviderInfos(self)->List[ModelProviderMeta]:
        return [v for k,v in self.ModelProvidersMeta.items()]
    def GetAllStandaloneModelNames(self)->List[str]:
        return [k for k in self.StandaloneModelsMeta]
    def GetAllBaselineModelNames(self)->List[str]:
        return [key for key,value in self.StandaloneModelsMeta.items() if value.IsBaseline==True]       #Limited to standalone models only for now.
    def GetAllModelKeys(self)->List[str]:
        return [k for k,v in self.ModelIndex.items()]
    def GetModelKeys(self, baselineFilter:Optional[bool] = None)->List[str]:       #TODO: add more filters here. ExcludeBaselines, FilterByModelName, ByProviderName etc.
        return [k for k,v in self.ModelIndex.items() if v.IsBaseline == baselineFilter and baselineFilter is not None]

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
            mp: ModelProviderBase = t.__new__(t)
            mp.__init__()
            meta = ModelProviderMeta(name, t, mp.ProviderAbbreviation())
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
    Print("FindKeysByFilters usage", factory.FindKeysByFilters(ModelFilters("ol","OllamaModelProvider", "llama3",False)))

    #Models Instance Creation
    Print("BaselineModels",     factory.CreateBaselineModels())
    Print("StandaloneModels",   factory.CreateStandaloneModels())
    Print("ModelProviders",     factory.CreateModelProviders())
    Print("AllEffectiveModels", factory.CreateAllModels())
    Print("CreateModelsByFilters() usage", factory.CreateModelsByFilters(ModelFilters("ol","OllamaModelProvider", "llama",False)))

    #usages
    Print("CreateModel(name) usage", factory.CreateModel("RandomModel"))
    Print("CreateModelProvider(name) usage",factory.CreateModelProvider("OllamaModelProvider"))
    Print("CreateModelsByProvider(name) usage",factory.CreateModelsByProvider("OllamaModelProvider"))
    Print("CreateModelByKey(key) usage via standalones", factory.CreateModelByKey("np.random"))
    Print("CreateModelByKey(key) usage via providers", factory.CreateModelByKey("ol.codellama"))