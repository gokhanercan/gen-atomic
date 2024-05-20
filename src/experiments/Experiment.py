from typing import List, Optional

from data.Dataset import UnitType
from models.ModelBase import ModelBase
from models.ModelFactory import ModelFactory
from providers.ProviderFactory import ProviderFactory
from units.UnitBase import UnitBase
from units.UnitFactory import UnitFactory
from utility import StringHelper


class Experiment(object):
    def __init__(self, unit:UnitBase, models:List[ModelBase] = None) -> None:
        super().__init__()
        self.Unit:UnitBase = unit
        self.Models:List[ModelBase] = models
        self.Name:Optional[str] = None

    def GetName(self)->str:
        return StringHelper.Coelesce(self.Name,self.Unit.UnitType.name)


class ExperimentFactory(object):
    def __init__(self) -> None:
        super().__init__()

    @staticmethod
    def CreateExperimentWithAllModels(unitType:UnitType)->Experiment:
        unit = UnitFactory().Create(unitType)
        models:List[ModelBase] = ModelFactory().CreateAllModels()
        exp:Experiment = Experiment(unit,models)
        return exp

    @staticmethod
    def CreateExperimentWithFakeModels(unitType:UnitType)->Experiment:
        unit = UnitFactory().Create(unitType)
        models:List[ModelBase] = ModelFactory().CreateFakeModels()
        exp:Experiment = Experiment(unit,models)
        return exp

    @staticmethod
    def CreateSingleModelExperiment(unitType: UnitType, providerName:str, modelConf:str) -> Experiment:
        unit = UnitFactory().Create(unitType)
        model: ModelBase = ModelFactory().Create(providerName,modelConf)
        exp: Experiment = Experiment(unit, [model])
        return exp

    @staticmethod
    def CreateProviderExperiment(unitType: UnitType, providerName:str) -> Experiment:
        unit = UnitFactory().Create(unitType)
        models: List[ModelBase] = ProviderFactory().CreateModelConfigurations(providerName)
        exp: Experiment = Experiment(unit,models)
        return exp