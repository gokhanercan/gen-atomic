import copy
from typing import List, Optional
from unittest import TestCase

from experiments.ModelConfiguration import ModelConfiguration, ModelConfigurations
from langunits.LangUnit import LangUnit
from langunits.LangUnitFactory import LangUnitFactory
from models.ModelBase import ModelBase
from models.ModelFactory import ModelFactory, ModelFilters
from models.StubModel import StubModel
from prompting.PromptingBase import PromptingBase, PromptingInfo
from prompting.decorators.prompt_decorator_base import (
    PromptDecoratorBase,
    PromptDecoratorInfo,
)
from prompting.impl.DirectPrompting import DirectPrompting
from prompting.prompting_factory import PromptingFactory
from prompting.repo.inmemory_prompt_repository import InMemoryPromptRepository
from prompting.repo.prompt_repository_base import PromptRepositoryBase
from utility import StringHelper
from itertools import combinations


class Experiment(object):
    def __init__(self, lang_unit: LangUnit, model_configs: ModelConfigurations = None) -> None:
        self.lang_unit: LangUnit = lang_unit  # we support single LangUnit per Experiment
        self.model_configs: ModelConfigurations = model_configs  # TODO: Too many model_configs drama!

    def get_models(self) -> List[ModelBase]:
        """
        Returns the flat list of model references in the experiment.
        :return: List[ModelBase]
        """
        if self.model_configs is None:
            raise ValueError("Model configurations are not set.")
        return self.model_configs.get_models()

    def get_model_by_key(self, model_key: str) -> ModelBase:
        """
        Returns the model reference by its model key.
        :return: ModelBase
        """
        if self.model_configs is None:
            raise ValueError("Model configurations are not set.")
        return [m for m in self.model_configs.get_models() if m.key() == model_key][0]

    def __repr__(self) -> str:
        try:
            return self.key()
        except Exception:
            return "<Experiment (repr failed)>"

    def __str__(self) -> str:
        return self.__repr__()

    def plain_name(self) -> str:
        return f"{self.lang_unit.name()}"

    def key(self) -> str:
        try:
            return f"E[{self.lang_unit}_{self.model_configs.key()}]"
        except Exception as e:
            return f"E[{self.lang_unit.name()}]"


class ExperimentFactory(object):

    def __init__(self, lang_unit_name: str, prompt_repo: PromptRepositoryBase, default_prompting: PromptingBase = None) -> None:
        super().__init__()
        self.lang_unit_name: str = lang_unit_name
        self.prompt_repo: PromptRepositoryBase = prompt_repo
        if default_prompting is None:
            default_prompting = PromptingFactory(prompt_repo).create_default(self.lang_unit_name)
        self.default_prompting: PromptingBase = default_prompting

    def create_experiment_with_all_models(self, prompting: PromptingBase | None = None) -> Experiment:
        unit: LangUnit = LangUnitFactory().create(self.lang_unit_name)
        models: List[ModelBase] = ModelFactory().create_all_models()
        eff_prompting: PromptingBase = prompting or self.default_prompting
        mcs = ModelConfigurations([ModelConfiguration(m, eff_prompting) for m in models])
        exp: Experiment = Experiment(unit, mcs)
        return exp

    def create_experiment_by_model_filters(
        self,
        mf: ModelFilters,
        include_baselines: bool = False,
        prompting: PromptingBase | None = None,
    ):
        unit: LangUnit = LangUnitFactory().create(self.lang_unit_name)
        model_factory = ModelFactory()
        models: List[ModelBase] = model_factory.create_models_by_filters(mf)
        if include_baselines:
            models += model_factory.create_baseline_models()
        eff_prompting: PromptingBase = prompting or self.default_prompting
        mcs = ModelConfigurations([ModelConfiguration(m, eff_prompting) for m in models])
        exp: Experiment = Experiment(unit, mcs)
        return exp

    def create_experiment_with_baseline_models(self, prompting: PromptingBase | None = None) -> Experiment:
        unit: LangUnit = LangUnitFactory().create(self.lang_unit_name)
        models: List[ModelBase] = ModelFactory().create_models_by_filters(ModelFilters(isBaseline=True))
        eff_prompting: PromptingBase = prompting or self.default_prompting
        mcs = ModelConfigurations([ModelConfiguration(m, eff_prompting) for m in models])
        exp: Experiment = Experiment(unit, mcs)
        return exp

    def create_single_model_experiment(self, model_key: str, prompting: PromptingBase | None = None) -> Experiment:
        unit: LangUnit = LangUnitFactory().create(self.lang_unit_name)
        model: ModelBase = ModelFactory().create_model_by_key(model_key)
        mcs: ModelConfigurations = ModelConfigurations([ModelConfiguration(model, prompting or self.default_prompting)])
        exp: Experiment = Experiment(unit, mcs)
        return exp

    def create_provider_experiment(
        self,
        provider_abbr: str,
        prompting: PromptingBase | None = None,
        include_baselines: bool = False,
    ) -> Experiment:
        unit: LangUnit = LangUnitFactory().Create(self.lang_unit_name)
        model_factory = ModelFactory()
        models: List[ModelBase] = model_factory.CreateModelsByFilters(ModelFilters(providerAbbr=provider_abbr))
        if include_baselines:
            models += model_factory.CreateBaselineModels()
        mcs: ModelConfigurations = ModelConfigurations(
            [ModelConfiguration(m, prompting or self.default_prompting) for m in models]
        )
        exp: Experiment = Experiment(unit, mcs)
        return exp

    def create_model_configurations_with_all_default_promptings(
        self, model_key: str, create_decorator_variations: bool = False
    ) -> List[ModelConfiguration]:
        model: ModelBase = ModelFactory().CreateModelByKey(model_key)
        p_factory = PromptingFactory(self.prompt_repo)
        lang_unit: LangUnit = LangUnitFactory().Create(self.lang_unit_name)
        p_metas: list[PromptingInfo] = p_factory.get_all_prompting_meta()
        mcs: list[ModelConfiguration] = []
        for p_meta in p_metas:
            p: PromptingBase = p_factory.create_prompting_instance(p_meta.key, lang_unit.CreateInfo())
            if isinstance(p, DirectPrompting) and create_decorator_variations:
                dp: DirectPrompting = p
                mcs.append(ModelConfiguration(model, dp))  # no decorators variant
                pds = list(p_factory.prompt_decorator_meta.values())
                pd_combinations = []
                for r in range(1, len(pds) + 1):
                    pd_combinations.extend(combinations(pds, r))
                for pd_comb in pd_combinations:
                    p_variant: DirectPrompting = copy.deepcopy(dp)
                    for pd in pd_comb:
                        pd: PromptDecoratorBase = p_factory.create_prompt_decorator_instance(pd.key)
                        p_variant.prompt_decorators.append(pd)
                    mcs.append(ModelConfiguration(model, p_variant))
            else:
                mcs.append(ModelConfiguration(model, p))
        return mcs

    def create_model_experiment_with_all_default_promptings(
        self, model_key: str, create_decorator_variations: bool = False
    ) -> Experiment:
        """
        Creates an experiment with a single model, and all promptings with their default settings and prompt texts.
        :param create_decorator_variations: If true, creates all possible prompt compositions.
        :param model_key:
        :return:
        """
        lang_unit: LangUnit = LangUnitFactory().Create(self.lang_unit_name)
        return Experiment(
            lang_unit,
            ModelConfigurations(
                self.create_model_configurations_with_all_default_promptings(model_key, create_decorator_variations)
            ),
        )


class ExperimentFactoryTests(TestCase):

    @property
    def _prompt_repo(self) -> PromptRepositoryBase:
        return InMemoryPromptRepository()

    def test_create_single_model_experiment__defaults_check_defaults(self):
        exp: Experiment = ExperimentFactory(
            "RegexVal", prompt_repo=self._prompt_repo, default_prompting=DirectPrompting("direct")
        ).create_single_model_experiment("np.stub")

        self.assertEqual(exp.LangUnit.Name(), "RegexVal")
        self.assertIsNotNone(exp.get_model_by_key("np.stub"))
        self.assertEqual(StubModel, type(exp.get_model_by_key("np.stub")))
        self.assertEqual(1, exp.model_configs.__len__())
        self.assertEqual(DirectPrompting, type(exp.model_configs.model_configs[0].prompting))

    def test_create_provider_experiment__customprompting__init_all(self):
        exp: Experiment = ExperimentFactory(
            "RegexVal", prompt_repo=self._prompt_repo, default_prompting=DirectPrompting("direct")
        ).create_provider_experiment("np")

        self.assertEqual(exp.LangUnit.Name(), "RegexVal")
        self.assertIsNotNone(exp.get_model_by_key("np.stub"))
        self.assertEqual(StubModel, type(exp.get_model_by_key("np.stub")))
        self.assertEqual(2, exp.model_configs.__len__())  # stub and random
        self.assertEqual(DirectPrompting, type(exp.model_configs.model_configs[0].prompting))


if __name__ == "__main__":

    lang_unit_name: str = "SqlSelect"
    repo: PromptRepositoryBase = InMemoryPromptRepository()
    e: Experiment = Experiment(
        LangUnitFactory().Create(lang_unit_name),
        ModelConfigurations(
            [
                ModelConfiguration(
                    ModelFactory().CreateModelByKey("np.stub"),
                    PromptingFactory(repo).create_default(lang_unit_name),
                ),
                ModelConfiguration(
                    ModelFactory().CreateModelByKey("np.random"),
                    PromptingFactory(repo).create_default(lang_unit_name),
                ),
            ]
        ),
    )
    print(e)
