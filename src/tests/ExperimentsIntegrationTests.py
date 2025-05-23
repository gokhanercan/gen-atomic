import unittest
from unittest import TestCase

from api.API import API
from data.Dataset import Dataset
from data.DatasetXmlRepository import DatasetXmlRepository
from experiments.Experiment import Experiment, ExperimentFactory
from experiments.ExperimentHost import ExperimentHost, ExperimentResults
from utility.Paths import Paths

class APISmokeTests(TestCase):
    def test_API_RunAllGetters(self):
        try:
            print(API().GetAllModelProviderNames())
            print(API().GetAllLangUnitNames())
        except Exception as e:
            self.fail(f"Some API getters failed with exception: {e}")

class ExperimentsIntegrationTest(TestCase):
    def test_ExperimentHost_AtomicDataset_RunExperiment(self):
        host:ExperimentHost = ExperimentHost()

        path:str = Paths().GetDataset("AtomicRegexValDataset")
        ds: Dataset = DatasetXmlRepository.Load(path)
        exp:Experiment = ExperimentFactory().CreateExperimentWithBaselineModels("RegexVal")

        # customize stub
        stubModel = [item for item in exp.Models if item.Name().__contains__("Stub")][0]
        fixedRegex: str = r"""^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$"""
        stubModel.StubUnit = fixedRegex  # type: ignore
        stubModel.StubName = "EmailStub"

        r:ExperimentResults = host.Run(exp,ds)
        r.Print(False)
        self.assertTrue(0 <= r.OverallAccuracy[0] <= 100)

if __name__ == "__main__":
    unittest.main()