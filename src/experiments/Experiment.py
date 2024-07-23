from typing import List, Optional

from langunits.LangUnit import LangUnit
from langunits.LangUnitFactory import LangUnitFactory
from models.ModelBase import ModelBase
from models.ModelFactory import ModelFactory
# from providers.ProviderFactory import ProviderFactory
from utility import StringHelper


class Experiment(object):
    def __init__(self, langUnit:LangUnit, models:List[ModelBase] = None) -> None:
        super().__init__()
        self.LangUnit:LangUnit = langUnit #We support single LangUnit per Experiment
        self.Models:List[ModelBase] = models
        self.Name:Optional[str] = None

    def GetName(self)->str:
        return StringHelper.Coelesce(self.Name,self.LangUnit.GetUnitType())


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
    def CreateExperimentWithFakeModels(langUnitName:str)->Experiment:
        unit:LangUnit = LangUnitFactory().Create(langUnitName)
        models:List[ModelBase] = ModelFactory().CreateFakeModels()
        exp:Experiment = Experiment(unit,models)
        return exp

    @staticmethod
    def CreateSingleModelExperiment(langUnitName:str, providerName:str, modelConf:str) -> Experiment:
        unit:LangUnit = LangUnitFactory().Create(langUnitName)
        model: ModelBase = ModelFactory().Create(providerName,modelConf)
        exp: Experiment = Experiment(unit, [model])
        return exp

    @staticmethod
    def CreateProviderExperiment(langUnitName:str, providerName:str) -> Experiment:
        unit:LangUnit = LangUnitFactory().Create(langUnitName)
        models: List[ModelBase] = ProviderFactory().CreateModelConfigurations(providerName)
        exp: Experiment = Experiment(unit,models)
        return exp

if __name__ == '__main__':
    print(ExperimentFactory().CreateExperimentWithAllModels("SqlSelect"))