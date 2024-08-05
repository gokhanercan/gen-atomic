from typing import List, Optional

from langunits.LangUnit import LangUnit
from langunits.LangUnitFactory import LangUnitFactory
from models.ModelBase import ModelBase
from models.ModelFactory import ModelFactory, ModelFilters
from prompting.Prompt import Prompt
from prompting.PromptingBase import PromptingBase
from prompting.SimplePrompting import SimplePrompting
# from providers.ProviderFactory import ProviderFactory
from utility import StringHelper


class Experiment(object):
    def __init__(self,langUnit:LangUnit, prompting:PromptingBase, models:List[ModelBase] = None) -> None:
        super().__init__()
        self.LangUnit:LangUnit = langUnit #We support single LangUnit per Experiment
        self.Models:List[ModelBase] = models
        self.Prompting:PromptingBase = prompting
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
    def CreateDefaultPrompting()->PromptingBase:
        instruction: str = (
            "Consider yourself a function that takes the input of asked validation {{langDesc}} statement, and "
            "your output should be a markdown code snippet formatted in the following schema, including "
            "the leading and trailing \"```{{langDesc}}\" and \"```\". Do not give me an explanation, only give "
            "me a {{langDesc}} expression. Do not add any additional characters.")
        promptTemplate: str = instruction + "\nAsked {{langDesc}} statement: {{description}}."

        defaultPrompting: PromptingBase = SimplePrompting(Prompt(promptTemplate))
        return defaultPrompting

    @staticmethod
    def CreateExperimentWithAllModels(langUnitName:str)->Experiment:
        unit:LangUnit = LangUnitFactory().Create(langUnitName)
        models:List[ModelBase] = ModelFactory().CreateAllModels()
        exp:Experiment = Experiment(unit,ExperimentFactory.CreateDefaultPrompting(),models)
        return exp

    @staticmethod
    def CreateExperimentByModelFilters(langUnitName:str, mf:ModelFilters, includeBaselines:bool = False):
        unit: LangUnit = LangUnitFactory().Create(langUnitName)
        modelFactory = ModelFactory()
        models: List[ModelBase] = modelFactory.CreateModelsByFilters(mf)
        if (includeBaselines): models += modelFactory.CreateBaselineModels()
        exp: Experiment = Experiment(unit,ExperimentFactory.CreateDefaultPrompting(), models)
        return exp

    @staticmethod
    def CreateExperimentWithBaselineModels(langUnitName:str)->Experiment:
        unit:LangUnit = LangUnitFactory().Create(langUnitName)
        models:List[ModelBase] = ModelFactory().CreateModelsByFilters(ModelFilters(isBaseline=True))
        exp:Experiment = Experiment(unit,ExperimentFactory.CreateDefaultPrompting(),models)
        return exp

    @staticmethod
    def CreateSingleModelExperiment(langUnitName:str, modelKey:str) -> Experiment:
        unit:LangUnit = LangUnitFactory().Create(langUnitName)
        model: ModelBase = ModelFactory().CreateModelByKey(modelKey)
        exp: Experiment = Experiment(unit,ExperimentFactory.CreateDefaultPrompting(), [model])
        return exp

    @staticmethod
    def CreateProviderExperiment(langUnitName:str, providerAbbr:str, includeBaselines:bool = False) -> Experiment:
        unit:LangUnit = LangUnitFactory().Create(langUnitName)
        modelFactory = ModelFactory()
        models: List[ModelBase] = modelFactory.CreateModelsByFilters(ModelFilters(providerAbbr=providerAbbr))
        if(includeBaselines): models += modelFactory.CreateBaselineModels()
        exp: Experiment = Experiment(unit,ExperimentFactory.CreateDefaultPrompting(),models)
        return exp

if __name__ == '__main__':
    print(ExperimentFactory().CreateExperimentWithAllModels("SqlSelect"))