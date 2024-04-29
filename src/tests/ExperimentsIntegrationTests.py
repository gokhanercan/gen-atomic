import unittest
from unittest import TestCase

from data.Dataset import Dataset, UnitType
from data.DatasetXmlRepository import DatasetXmlRepository
from experiments.Experiment import Experiment, ExperimentFactory
from experiments.ExperimentHost import ExperimentHost, ExperimentResults
from utility.PathHelper import PathHelper


class ExperimentsIntegrationTest(TestCase):
    def test_ExperimentHost_AtomicDataset_RunExperiment(self):
        host:ExperimentHost = ExperimentHost()

        path:str = PathHelper().GetDataset("AtomicDataset")
        ds: Dataset = DatasetXmlRepository.Load(path)
        exp:Experiment = ExperimentFactory().CreateExperimentWithAllModels(UnitType.RegexVal)

        # customize stub
        stubModel = [item for item in exp.Models if item.ModelName().__contains__("Stub")][0]
        fixedRegex: str = r"""^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$"""
        stubModel.StubUnit = fixedRegex  # type: ignore
        stubModel.StubName = "EmailStub"

        r:ExperimentResults = host.Run(exp,ds.Units)

        self.assertTrue(0 <= r.OverallAccuracy[0] <= 100)

if __name__ == "__main__":
    unittest.main()