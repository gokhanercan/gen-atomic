from data.Dataset import UnitType
from models.ModelBase import ModelBase
from models.ModelStub import ModelStub
from units.UnitBase import UnitBase
from units.UnitFactory import UnitFactory

class Experiment(object):
    def __init__(self, unit:UnitBase, model:ModelBase) -> None:
        super().__init__()
        self.Unit:UnitBase = unit
        self.Model:ModelBase = model

class ExperimentFactory(object):
    def __init__(self) -> None:
        super().__init__()

    def CreateExperiment(self, unitType:UnitType)->Experiment:
        unit = UnitFactory().Create(unitType)
        modelStub = ModelStub()     #TODO: bind real models here.
        exp:Experiment = Experiment(unit,modelStub)
        return exp

