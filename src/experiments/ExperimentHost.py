from typing import Optional, List

from data.Dataset import Dataset, UnitType
from data.DatasetXmlRepository import DatasetXmlRepository
from experiments.Experiment import Experiment, ExperimentFactory
from pandas import DataFrame  # type: ignore
from tabulate import tabulate  # type: ignore

from utility.FormatHelper import FormatHelper
from utility.Paths import Paths


class ExperimentResults(object):

    def __init__(self, **kwargs) -> None:
        super().__init__()
        self.OverallAccuracy:List = None
        for key, value in kwargs.items():
            setattr(self, key, value)


class ExperimentHost(object):

    def Run(self, exp: Experiment, fields):

        dfAggr = DataFrame()
        for model in exp.Models:
            dfCases: DataFrame = DataFrame()
            fieldIndex: int = 1
            caseIndex: int = 1
            passedCaseCount: int = 0
            totalCaseCount: int = 0
            ccCount: int = 0
            icCount: int = 0
            ccPassed: int = 0
            icPassed: int = 0

            for f in fields:
                generated: str = model.Generate(f.Description)
                for cc in f.CorrectCases:
                    dfCases.at[caseIndex, "Type"] = f.UnitType.name
                    dfCases.at[caseIndex, "Name"] = f.Name
                    dfCases.at[caseIndex, "Case"] = "CC-> " + cc
                    passed:bool = exp.Unit.RunTest(generated, cc)
                    dfCases.at[caseIndex, "Passed"] = "OK" if passed else "X"
                    dfCases.at[caseIndex, "Generated Code"] = FormatHelper.FormatCode(generated, 20)
                    if (passed):
                        passedCaseCount = passedCaseCount + 1
                        ccPassed = ccPassed + 1
                    dfCases.at[caseIndex, "Desc"] = f.Description
                    totalCaseCount = totalCaseCount + 1
                    ccCount = ccCount + 1
                    caseIndex += 1
                for icc in f.IncorrectCases:
                    dfCases.at[caseIndex, "Type"] = f.UnitType.name
                    dfCases.at[caseIndex, "Name"] = f.Name
                    dfCases.at[caseIndex, "Case"] = "IC-> " + icc
                    passed:bool = not exp.Unit.RunTest(generated, icc)  # type: ignore
                    dfCases.at[caseIndex, "Passed"] = "OK" if passed else "X"
                    dfCases.at[caseIndex, "Generated Code"] = FormatHelper.FormatCode(generated, 20)
                    if (passed):
                        passedCaseCount = passedCaseCount + 1
                        icPassed = icPassed + 1
                    dfCases.at[caseIndex, "Desc"] = f.Description
                    totalCaseCount = totalCaseCount + 1
                    icCount = icCount + 1
                    caseIndex += 1
                fieldIndex += 1

            print(f"\n-- {model.ModelName().upper()} MODEL RESULTS --")
            print(tabulate(dfCases, headers="keys", tablefmt='psql', floatfmt=".2f"))

            # region Aggr Reports
            # TODO:Report confusion matrix for binary schemas
            # TODO:Report accuracy by type and field also.

            accuracyColName = f"{model.ModelName()} (%)"
            ccAccuracy: float = (float(ccPassed) / float(ccCount)) * 100
            dfAggr.at["CorrectCase", accuracyColName] = ccAccuracy

            icAccuracy: float = (float(icPassed) / float(icCount)) * 100
            dfAggr.at["IncorrectCase", accuracyColName] = icAccuracy

            overallAccuracy: float = (float(passedCaseCount) / float(totalCaseCount)) * 100
            dfAggr.at["Overall", accuracyColName] = overallAccuracy
            # endregion

        experimentHeader = f"-- {exp.GetName().upper()} EXPERIMENT --"
        print("\n" + experimentHeader)
        print(tabulate(dfAggr, headers="keys", tablefmt='psql', floatfmt=".2f"))
        overallAccuracy:List = dfAggr.iloc[-1]
        return ExperimentResults(OverallAccuracy=overallAccuracy)


if __name__ == '__main__':
    path = Paths().GetDataset("AtomicDataset")
    ds: Dataset = DatasetXmlRepository.Load(path)
    exp: Experiment = ExperimentFactory.CreateExperimentWithAllModels(UnitType.RegexVal)

    # customize stub
    stubModel = [item for item in exp.Models if item.ModelName().__contains__("Stub")][0]
    fixedRegex: str = r"""^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$"""
    stubModel.StubUnit = fixedRegex  # type: ignore
    stubModel.StubName = "EmailStub"

    r:ExperimentResults = ExperimentHost().Run(exp, ds.Units)
