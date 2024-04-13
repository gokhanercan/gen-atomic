from data.Dataset import Dataset, UnitType
from experiments.ExperimentFactory import Experiment, ExperimentFactory


class ExperimentHost(object):        #TODO: Load ds here.https://github.com/users/gokhanercan/projects/3/views/1?pane=issue&itemId=58244903

    def Run(self, exp:Experiment, fields):
        # TODO: dataframe here for easier reporting
        passedCaseCount:int = 0
        totalCaseCount: int = 0
        for f in fields:
            generated:str = exp.Model.Generate(f.Description)
            for cc in f.CorrectCases:
                passed:bool = exp.Unit.RunTest(generated,cc)
                if(passed): passedCaseCount = passedCaseCount + 1
                totalCaseCount = totalCaseCount + 1
                if(passed):
                    print("[Passed] Field '" + str(f) + "':" + "with regex '" + generated + "' for correct case " + cc)
                else:
                    print("[Failed] Field '" + str(f) + "':" + "with regex '" + generated + "' for correct case " + cc)
            #TODO: Impl incorrect cases

        print("Overall accuracy:" + str((float(passedCaseCount) / float(totalCaseCount)) * 100))


if __name__ == '__main__':

    ds:Dataset = Dataset.SampleRegexValDataset()
    exp:Experiment = ExperimentFactory().CreateExperiment(UnitType.RegexVal)

    #stub
    fixedRegex: str = """^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$"""
    exp.Model.StubUnit = fixedRegex

    ExperimentHost().Run(exp,ds.Units)