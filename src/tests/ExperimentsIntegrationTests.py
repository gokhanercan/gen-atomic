import unittest
from unittest import TestCase

from data.Dataset import Dataset, UnitType
from data.DatasetXmlRepository import DatasetXmlRepository
from experiments.ExperimentFactory import Experiment, ExperimentFactory
from experiments.ExperimentHost import ExperimentHost, ExperimentResults


class ExperimentsIntegrationTest(TestCase):
    def test_ExperimentHost_AtomicDataset_RunExperiment(self):
        host:ExperimentHost = ExperimentHost()

        #region Relative Path
        # TODO: Make it accessible from every context. Currently it is optimized for running through pytest form the outer scope. https://github.com/users/gokhanercan/projects/3/views/1?pane=issue&itemId=59674842
        #import os
        #cwd = os.getcwd()       #tests folder
        #parent = os.path.dirname(os.path.dirname(cwd))  #two parents
        #path = parent + "\\" + "data\\AtomicDataset.xml"
        #endregion

        path = "data\\AtomicDataset.xml"        #relation to project root. not src root.
        ds: Dataset = DatasetXmlRepository.Load(path)
        exp:Experiment = ExperimentFactory().CreateExperiment(UnitType.RegexVal)
        exp.Model.StubUnit = r"""^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$"""
        r:ExperimentResults = host.Run(exp,ds.Units)
        self.assertTrue(0 <= r.OverallAccuracy <= 100)

if __name__ == "__main__":
    unittest.main()