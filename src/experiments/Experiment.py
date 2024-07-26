from typing import List, Optional

from langunits.LangUnit import LangUnit
from langunits.LangUnitFactory import LangUnitFactory
from models.ModelBase import ModelBase
from models.ModelFactory import ModelFactory, ModelFilters
# from providers.ProviderFactory import ProviderFactory
from utility import StringHelper


class Experiment(object):
    def __init__(self, langUnit:LangUnit, models:List[ModelBase] = None) -> None:
        super().__init__()
        self.LangUnit:LangUnit = langUnit #We support single LangUnit per Experiment
        self.Models:List[ModelBase] = models
        self.Name:Optional[str] = None

    def GetName(self)->str:
        return StringHelper.Coelesce(self.Name,self.LangUnit.Name())

    def __str__(self) -> str:
        return f"E[{self.LangUnit}]"
    def __repr__(self) -> str:
        return self.__str__()


class ExperimentFactory(object):
    def __init__(self) -> None:
        super().__init__()

    @staticmethod
    def CreateExperimentWithAllModels(langUnitName:str)->Experiment:
        unit:LangUnit = LangUnitFactory().Create(langUnitName)
        models:List[ModelBase] = ModelFactory().CreateAllModels()
        exp:Experiment = Experiment(unit,models)
        return exp

    @staticmethod
    def CreateExperimentWithBaselineModels(langUnitName:str)->Experiment:
        unit:LangUnit = LangUnitFactory().Create(langUnitName)
        models:List[ModelBase] = ModelFactory().CreateModelsByFilters(ModelFilters(IsBaseline=True))
        exp:Experiment = Experiment(unit,models)
        return exp

    @staticmethod
    def CreateSingleModelExperiment(langUnitName:str, modelKey:str) -> Experiment:
        unit:LangUnit = LangUnitFactory().Create(langUnitName)
        model: ModelBase = ModelFactory().CreateModelByKey(modelKey)
        exp: Experiment = Experiment(unit, [model])
        return exp

    @staticmethod
    def CreateProviderExperiment(langUnitName:str, providerAbbr:str, includeBaselines:bool = False) -> Experiment:
        unit:LangUnit = LangUnitFactory().Create(langUnitName)
        modelFactory = ModelFactory()
        models: List[ModelBase] = modelFactory.CreateModelsByFilters(ModelFilters(providerAbbr=providerAbbr))
        if(includeBaselines): models += modelFactory.CreateBaselineModels()
        exp: Experiment = Experiment(unit,models)
        return exp

if __name__ == '__main__':
    print(ExperimentFactory().CreateExperimentWithAllModels("SqlSelect"))