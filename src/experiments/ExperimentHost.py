import time
from typing import Optional, List, Dict

from data.Dataset import Dataset, Unit, Criteria, Constraint
from data.DatasetXmlRepository import DatasetXmlRepository
from experiments.Experiment import Experiment, ExperimentFactory
from pandas import DataFrame  # type: ignore
from tabulate import tabulate  # type: ignore
from colorama import Fore

from langunits.LangUnit import LangUnitInfo
from models.ModelFactory import ModelFactory, ModelFilters
from utility.FormatHelper import FormatHelper
from utility.Paths import Paths


class ExperimentResults(object):

    def __init__(self, experimentName:str, **kwargs) -> None:
        super().__init__()
        self.ExperimentName:str = experimentName
        self.ModelResults:Dict[str,DataFrame] = {}
        self.Results:DataFrame = Optional[DataFrame]
        self.OverallAccuracy:List = Optional[List]
        for key, value in kwargs.items():
            setattr(self, key, value)

    def Print(self, ignoreFakeModelReports = True):
        if(self.ModelResults is not None):
            fakeModelNames = ModelFactory().GetAllBaselineModelNames()
            for modelConf,df in self.ModelResults.items():
                if(ignoreFakeModelReports):
                    if(fakeModelNames.__contains__(modelConf)): continue
                    if(modelConf.__contains__("Stub")): continue
                    if(modelConf.__contains__("Random")): continue
                print(f"\n-- {modelConf.upper()} MODEL RESULTS --")
                #region styling
                # for index, row in df.iterrows():
                #     if row['Passed'] == "OK":
                #         df.at[index, 'Passed'] = f"{Fore.GREEN}OK{Fore.RESET}"
                #         df.at[index, 'Case'] = f"{Fore.GREEN}{row['Case']}{Fore.RESET}"
                #     if row['Passed'] == "X":
                #         df.at[index, 'Passed'] = f"{Fore.RED}X{Fore.RESET}"
                #         df.at[index, 'Case'] = f"{Fore.RED}{row['Case']}{Fore.RESET}"
                #endregion
                print(tabulate(df, headers="keys", tablefmt='grid', floatfmt=".2f"))
        if(self.Results is not None):
            experimentHeader = f"-- {self.ExperimentName.upper()} EXPERIMENT --"
            print("\n" + experimentHeader)
            print(tabulate(self.Results, headers="keys", tablefmt='psql', floatfmt=".2f"))


class ExperimentHost(object):

    def Run(self, exp: Experiment, ds:Dataset, formatCode:bool = False):
        start_time = time.time()
        print(f"Running experiment on {ds.Name} dataset with {str(len(exp.Models))} model configuration(s) ...")

        modelResults:Dict[str,DataFrame] = {}

        dfAggr = DataFrame()
        for model in exp.Models:
            model_start_time = time.time()
            print(f"\tRunning model {model.Key()} on {ds.Name} dataset ...")
            dfCases: DataFrame = DataFrame()
            fieldIndex: int = 1
            caseIndex: int = 1
            passedCaseCount: int = 0
            totalCaseCount: int = 0
            ccCount: int = 0
            icCount: int = 0
            ccPassed: int = 0
            icPassed: int = 0

            y_true: List[int] = []
            y_pred: List[int] = []

            for f in ds.Units:
                #region Constraints
                langUnitInfo:LangUnitInfo = exp.LangUnit.CreateInfo()
                generated: str = model.Generate(f.Description,langUnitInfo)
                passed: bool = exp.LangUnit.RunTest(generated, "", f)

                dfCases.at[caseIndex, "Type"] = f.UnitType
                dfCases.at[caseIndex, "Name"] = f.Name
                dfCases.at[caseIndex, "Passed"] = "OK" if passed else "X"
                dfCases.at[caseIndex, "Generated Code"] = FormatHelper.ShortenCode(generated,20) if formatCode else generated
                if (passed):
                    passedCaseCount = passedCaseCount + 1
                    ccPassed = ccPassed + 1
                dfCases.at[caseIndex, "Desc"] = f.Description
                totalCaseCount = totalCaseCount + 1
                ccCount = ccCount + 1
                caseIndex += 1

                y_true.append(1)
                y_pred.append(int(passed))
                #endregion

                #region Cases
                for cc in f.CorrectCases:
                    dfCases.at[caseIndex, "Type"] = f.UnitType
                    dfCases.at[caseIndex, "Name"] = f.Name
                    dfCases.at[caseIndex, "Case"] = "CC-> " + cc
                    passed:bool = exp.LangUnit.RunTest(generated, cc, f)
                    dfCases.at[caseIndex, "Passed"] = "OK" if passed else "X"
                    dfCases.at[caseIndex, "Generated Code"] = FormatHelper.ShortenCode(generated, 20) if formatCode else generated
                    if (passed):
                        passedCaseCount = passedCaseCount + 1
                        ccPassed = ccPassed + 1
                    dfCases.at[caseIndex, "Desc"] = f.Description
                    totalCaseCount = totalCaseCount + 1
                    ccCount = ccCount + 1
                    caseIndex += 1
                    y_true.append(1)
                    y_pred.append(int(passed))
                for icc in f.IncorrectCases:
                    dfCases.at[caseIndex, "Type"] = f.UnitType
                    dfCases.at[caseIndex, "Name"] = f.Name
                    dfCases.at[caseIndex, "Case"] = "IC-> " + icc
                    passed:bool = not exp.LangUnit.RunTest(generated, icc, f)  # type: ignore
                    dfCases.at[caseIndex, "Passed"] = "OK" if passed else "X"
                    dfCases.at[caseIndex, "Generated Code"] = FormatHelper.ShortenCode(generated, 20) if formatCode else generated
                    if (passed):
                        passedCaseCount = passedCaseCount + 1
                        icPassed = icPassed + 1
                    dfCases.at[caseIndex, "Desc"] = f.Description
                    totalCaseCount = totalCaseCount + 1
                    icCount = icCount + 1
                    caseIndex += 1
                    y_true.append(0)
                    y_pred.append(int(not passed))
                fieldIndex += 1
                #endregion

            model_end_time = time.time()
            model_elapsed_time = model_end_time - model_start_time
            print(f"\tExperiment for model {model.Key()} is completed in {self.format_time(model_elapsed_time)} seconds.", )
            modelResults[model.Key()] = dfCases

            accuracyColName = f"{model.Key()} (%)"
            #if(ccCount + icCount + len(f.Conditions) == 0): raise Exception("No cases defined in the dataset!") TODO: commented because of a lack of Conditions implementation
            ccAccuracy: float = (float(ccPassed) / float(ccCount)) * 100 if ccCount > 0 else 0
            dfAggr.at["CorrectCase", accuracyColName] = ccAccuracy

            overallAccuracy: float = (float(passedCaseCount) / float(totalCaseCount)) * 100 if totalCaseCount > 0 else 0
            dfAggr.at["Overall", accuracyColName] = overallAccuracy

            #region Precision, Recall, F1 Score

            from sklearn.metrics import precision_score, recall_score, f1_score

            # Calculate precision, recall, and F1-score
            dfAggr.at["Precision", accuracyColName] = precision_score(y_true, y_pred, zero_division=0) * 100
            dfAggr.at["Recall", accuracyColName] = recall_score(y_true, y_pred, zero_division=0) * 100
            dfAggr.at["F1 Score", accuracyColName] =  f1_score(y_true, y_pred, zero_division=0) * 100
            #endregion

        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Experiment is completed in {self.format_time(elapsed_time)} seconds.", )

        overallAccuracy:List = dfAggr.iloc[-1]

        r = ExperimentResults(exp.GetName(), OverallAccuracy=overallAccuracy)
        r.ModelResults = modelResults
        r.Results = dfAggr
        return r

    def format_time(self,seconds):
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return "{:02}:{:02}:{:02}".format(int(hours), int(minutes), int(seconds))

def RunSQLSelectExperiment():
    #Dataset
    path = Paths().GetDataset("AtomicSQLSelectDataset")
    ds: Dataset = DatasetXmlRepository.Load(path)

    exp = ExperimentFactory().CreateExperimentByModelFilters("SqlSelect",ModelFilters(providerAbbr="ol", keyContains="codellama"),includeBaselines=False)

    #region baselines stubbing
    #stubModel = [item for item in exp.Models if item.Name().__contains__("Stub")][0]
    #stubModel.StubUnit = "select * from Products"
    #stubModel.StubName = "SQLStub"
    #endregion

    r: ExperimentResults = ExperimentHost().Run(exp, ds, formatCode=False)
    r.Print()
    ds.Print()

def RunRegexValExperiment():
    #Dataset
    path = Paths().GetDataset("AtomicSQLSelectDataset")
    ds: Dataset = DatasetXmlRepository.Load(path)

    #Exp. Context
    exp = ExperimentFactory().CreateExperimentByModelFilters("SqlSelect",ModelFilters(keyContains="codellama"),includeBaselines=False)

    #region baselines stubbing
    stubs = [item for item in exp.Models if item.Name().__contains__("Stub")]
    if(stubs):
        stubModel = stubs[0]
        fixedRegex: str = r"""^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$"""
        stubModel.StubUnit = fixedRegex  # type: ignore
        stubModel.StubName = "EmailStub"
    #endregion

    r:ExperimentResults = ExperimentHost().Run(exp, ds, formatCode=True)
    r.Print()
    # ds.Print()

if __name__ == '__main__':
    RunSQLSelectExperiment()
    #RunRegexValExperiment()