import inspect
import unittest
from unittest import TestCase

from data.Dataset import Dataset
from data.DatasetXmlRepository import DatasetXmlRepository
from experiments.Experiment import Experiment, ExperimentFactory
from experiments.ExperimentHost import ExperimentHost, ExperimentResults
from models.StubModel import StubModel
from prompting.repo.inmemory_prompt_repository import InMemoryPromptRepository
from utility.Paths import Paths


# noinspection PyMethodMayBeStatic
class APISmokeTests(TestCase):

    def test_api_run_all_get_functions(self):
        from api.api import API

        api = API()
        for name, method in inspect.getmembers(api, predicate=inspect.ismethod):
            if name.lower().startswith("get"):
                sig = inspect.signature(method)
                if all(
                    p.default != inspect.Parameter.empty
                    or p.kind == inspect.Parameter.VAR_POSITIONAL
                    or p.kind == inspect.Parameter.VAR_KEYWORD
                    for p in sig.parameters.values()
                ):
                    # Safe to call if all parameters have defaults or are *args/**kwargs
                    result = method()
                    assert isinstance(result, list) or isinstance(result, str)


class ExperimentsIntegrationTest(TestCase):

    def test_ExperimentHost_AtomicDataset_RunExperiment(self):
        host: ExperimentHost = ExperimentHost()

        path: str = Paths().GetDataset("AtomicRegexValDataset")
        ds: Dataset = DatasetXmlRepository.Load(path)
        exp: Experiment = ExperimentFactory(
            "RegexVal", InMemoryPromptRepository()
        ).create_experiment_with_baseline_models()

        stubs = [item for item in exp.get_models() if isinstance(item, StubModel)]
        StubModel.fake_email(stubs)

        r: ExperimentResults = host.Run(exp, ds)
        r.Print(False)
        self.assertTrue(0 <= r.OverallAccuracy.iloc[0] <= 100)


if __name__ == "__main__":
    unittest.main()
