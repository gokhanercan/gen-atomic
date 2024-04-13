from data.Dataset import Dataset, UnitType
from experiments.ExperimentFactory import Experiment, ExperimentFactory
from pandas import DataFrame
from tabulate import tabulate

from utility.FormatHelper import FormatHelper


class ExperimentHost(
    object):  # TODO: Load ds here.https://github.com/users/gokhanercan/projects/3/views/1?pane=issue&itemId=58244903

    def Run(self, exp: Experiment, fields):
        dfCases: DataFrame = DataFrame()
        fieldIndex: int = 1
        caseIndex: int = 1
        passedCaseCount: int = 0
        totalCaseCount: int = 0

        for f in fields:
            generated: str = exp.Model.Generate(f.Description)
            for cc in f.CorrectCases:
                dfCases.at[caseIndex, "Type"] = f.UnitType.name
                dfCases.at[caseIndex, "Name"] = f.Name
                dfCases.at[caseIndex, "Case"] = "CC-> " + cc
                passed: bool = exp.Unit.RunTest(generated, cc)
                dfCases.at[caseIndex, "Passed"] = "OK" if passed else "X"
                dfCases.at[caseIndex, "Generated Code"] = FormatHelper.FormatCode(generated, 20)
                if (passed): passedCaseCount = passedCaseCount + 1
                dfCases.at[caseIndex, "Desc"] = f.Description
                totalCaseCount = totalCaseCount + 1
                caseIndex += 1
            for icc in f.IncorrectCases:
                dfCases.at[caseIndex, "Type"] = f.UnitType.name
                dfCases.at[caseIndex, "Name"] = f.Name
                dfCases.at[caseIndex, "Case"] = "IC-> " + icc
                passed: bool = exp.Unit.RunTest(generated, icc)
                dfCases.at[caseIndex, "Passed"] = "OK" if passed else "X"
                dfCases.at[caseIndex, "Generated Code"] = FormatHelper.FormatCode(generated, 20)
                if (passed): passedCaseCount = passedCaseCount + 1
                dfCases.at[caseIndex, "Desc"] = f.Description
                totalCaseCount = totalCaseCount + 1
                caseIndex += 1
            fieldIndex += 1

        print("\n-- CASE RESULTS --")
        print(tabulate(dfCases, headers="keys", tablefmt='psql', floatfmt=".2f"))

        # TODO:Report confusion matrix.
        # TODO: Report accuracy by type and field also.
        print("Overall accuracy:" + str((float(passedCaseCount) / float(totalCaseCount)) * 100))


if __name__ == '__main__':
    ds: Dataset = Dataset.SampleRegexValDataset()
    exp: Experiment = ExperimentFactory().CreateExperiment(UnitType.RegexVal)

    # stub
    fixedRegex: str = r"""^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$"""
    exp.Model.StubUnit = fixedRegex

    ExperimentHost().Run(exp, ds.Units)
