from typing import List, Optional
from unittest import TestCase

from experiments.ModelConfiguration import ModelConfiguration, ModelConfigurations
from langunits.LangUnit import LangUnit
from langunits.LangUnitFactory import LangUnitFactory
from models.ModelBase import ModelBase
from models.ModelFactory import ModelFactory, ModelFilters
from models.StubModel import StubModel
from prompting.PromptingBase import PromptingBase
from prompting.impl.DirectPrompting import DirectPrompting
from prompting.prompting_factory import PromptingFactory
from utility import StringHelper


class Experiment(object):
    # def __init__(self, langUnit: LangUnit, models: List[ModelBase] = None) -> None:
    def __init__(self, langUnit:LangUnit, model_configs:ModelConfigurations = None) -> None:
        self.LangUnit:LangUnit = langUnit #We support single LangUnit per Experiment
        # self.Models:List[ModelBase] = models    #TODO:OBSOLETE:That should be model configuration including Prompting and other settings!
        self.model_configs:ModelConfigurations = model_configs      #TODO: Too many model_configs drama!
        # self.Name:Optional[str] = None

    # def GetName(self)->str:
    #     return StringHelper.Coelesce(self.Name,self.LangUnit.Name())

    def get_models(self) -> List[ModelBase]:
        """
        Returns the flat list of model references in the experiment.
        :return: List[ModelBase]
        """
        if self.model_configs is None:
            raise ValueError("Model configurations are not set.")
        return self.model_configs.get_models()

    def get_model_by_key(self, model_key:str) -> ModelBase:
        """
        Returns the model reference by its model key.
        :return: ModelBase
        """
        if self.model_configs is None:
            raise ValueError("Model configurations are not set.")
        return [m for m in self.model_configs.get_models() if m.Key() == model_key][0]

    def __repr__(self) -> str:
        try:
            return self.key()
        except Exception:
            return "<Experiment (repr failed)>"

    def __str__(self) -> str:
        return self.__repr__()

    def plain_name(self) -> str:
        return f"{self.LangUnit.Name()}"

    def key(self) -> str:
        try:
            return f"E[{self.LangUnit}_{self.model_configs.key()}]"
        except Exception as e:
            return f"E[{self.LangUnit.Name()}]"
        # return f"{self.LangUnit.Name()}_{self.GetName()}"


class ExperimentFactory(object):

    def __init__(self, lang_unit_name:str, default_prompting:PromptingBase = None) -> None:
        super().__init__()
        self.lang_unit_name: str = lang_unit_name
        if(default_prompting is None):
            default_prompting = PromptingFactory().create_default(self.lang_unit_name)
        self.default_prompting:PromptingBase = default_prompting

    def create_experiment_with_all_models(self, prompting:PromptingBase | None = None)->Experiment:
        unit:LangUnit = LangUnitFactory().Create(self.lang_unit_name)
        models:List[ModelBase] = ModelFactory().CreateAllModels()
        eff_prompting: PromptingBase = prompting or self.default_prompting
        mcs = ModelConfigurations([ModelConfiguration(m, eff_prompting) for m in models])
        exp:Experiment = Experiment(unit,mcs)
        return exp

    def create_experiment_by_model_filters(self, mf:ModelFilters, include_baselines:bool = False, prompting: PromptingBase | None = None):
        unit: LangUnit = LangUnitFactory().Create(self.lang_unit_name)
        model_factory = ModelFactory()
        models: List[ModelBase] = model_factory.CreateModelsByFilters(mf)
        if (include_baselines):
            models += model_factory.CreateBaselineModels()
        eff_prompting:PromptingBase = prompting or self.default_prompting
        mcs = ModelConfigurations([ModelConfiguration(m,eff_prompting) for m in models])
        exp: Experiment = Experiment(unit,mcs)
        return exp

    def create_experiment_with_baseline_models(self, prompting:PromptingBase | None = None)->Experiment:
        unit:LangUnit = LangUnitFactory().Create(self.lang_unit_name)
        models:List[ModelBase] = ModelFactory().CreateModelsByFilters(ModelFilters(isBaseline=True))
        eff_prompting: PromptingBase = prompting or self.default_prompting
        mcs = ModelConfigurations([ModelConfiguration(m, eff_prompting) for m in models])
        exp:Experiment = Experiment(unit,mcs)
        return exp

    def create_single_model_experiment(self, model_key:str, prompting:PromptingBase | None = None) -> Experiment:
        unit:LangUnit = LangUnitFactory().Create(self.lang_unit_name)
        model: ModelBase = ModelFactory().CreateModelByKey(model_key)
        mcs: ModelConfigurations = ModelConfigurations([ModelConfiguration(model, prompting or self.default_prompting)])
        exp: Experiment = Experiment(unit, mcs)
        return exp

    def create_provider_experiment(self, provider_abbr:str, prompting: PromptingBase | None = None, include_baselines:bool = False) -> Experiment:
        unit:LangUnit = LangUnitFactory().Create(self.lang_unit_name)
        model_factory = ModelFactory()
        models: List[ModelBase] = model_factory.CreateModelsByFilters(ModelFilters(providerAbbr=provider_abbr))
        if(include_baselines):
            models += model_factory.CreateBaselineModels()
        mcs: ModelConfigurations = ModelConfigurations([ModelConfiguration(m,prompting or self.default_prompting) for m in models])
        exp: Experiment = Experiment(unit,mcs)
        return exp

class ExperimentFactoryTests(TestCase):

    def test_create_single_model_experiment__defaults_checkDefaults(self):
        exp:Experiment = ExperimentFactory("RegexVal",
                                           default_prompting=DirectPrompting("direct")).create_single_model_experiment(
            "np.stub")

        self.assertEqual(exp.LangUnit.Name(), "RegexVal")
        self.assertIsNotNone (exp.get_model_by_key("np.stub"))
        self.assertEqual(StubModel,type(exp.get_model_by_key("np.stub")))
        self.assertEqual(1,exp.model_configs.__len__())
        self.assertEqual(DirectPrompting, type(exp.model_configs.model_configs[0].prompting))

    def test_create_provider_experiment__todoname(self):
        exp:Experiment = ExperimentFactory("RegexVal",default_prompting=DirectPrompting("direct")).create_provider_experiment("np")

        self.assertEqual(exp.LangUnit.Name(), "RegexVal")
        self.assertIsNotNone (exp.get_model_by_key("np.stub"))
        self.assertEqual(StubModel,type(exp.get_model_by_key("np.stub")))
        self.assertEqual(2,exp.model_configs.__len__()) #stub and random
        self.assertEqual(DirectPrompting, type(exp.model_configs.model_configs[0].prompting))


if __name__ == '__main__':

    lang_unit_name:str = "SqlSelect"
    e:Experiment = Experiment(LangUnitFactory().Create(lang_unit_name),
                              ModelConfigurations(
                                    [
                                    ModelConfiguration(ModelFactory().CreateModelByKey("np.stub"),PromptingFactory().create_default(lang_unit_name)),
                                    ModelConfiguration(ModelFactory().CreateModelByKey("np.random"),PromptingFactory().create_default(lang_unit_name))
                                    ]
                              )
                   )
    print(e)
