import time
from typing import Optional, List, Dict

from data.Dataset import Dataset, UnitType, Unit, Criteria, Condition
from data.DatasetXmlRepository import DatasetXmlRepository
from experiments.Experiment import Experiment, ExperimentFactory
from pandas import DataFrame  # type: ignore
from tabulate import tabulate  # type: ignore
from colorama import Fore

from models.ModelBase import ModelConf
from models.ModelFactory import ModelFactory
from providers.OllamaModelProvider import OllamaModelProvider
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
            fakeModelNames = ModelFactory().ListFakeModelNames()
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
            modelConf: str = f"{model.ProviderName()}-{model.ModelName()}"
            model_start_time = time.time()
            print(f"\tRunning model {modelConf} on {ds.Name} dataset ...")
            dfCases: DataFrame = DataFrame()
            fieldIndex: int = 1
            caseIndex: int = 1
            passedCaseCount: int = 0
            totalCaseCount: int = 0
            ccCount: int = 0
            icCount: int = 0
            ccPassed: int = 0
            icPassed: int = 0

            for f in ds.Units:
                #Conditions
                generated: str = model.Generate(f.Description)
                passed: bool = exp.Unit.RunTest(generated, None, f.Conditions)

                dfCases.at[caseIndex, "Type"] = f.UnitType.name
                dfCases.at[caseIndex, "Name"] = f.Name
                #dfCases.at[caseIndex, "Cond"] = "CC-> " + cc
                dfCases.at[caseIndex, "Passed"] = "OK" if passed else "X"
                dfCases.at[caseIndex, "Generated Code"] = FormatHelper.ShortenCode(generated,20) if formatCode else generated
                if (passed):
                    passedCaseCount = passedCaseCount + 1
                    ccPassed = ccPassed + 1
                dfCases.at[caseIndex, "Desc"] = f.Description
                totalCaseCount = totalCaseCount + 1
                ccCount = ccCount + 1
                caseIndex += 1

                #region Cases
                for cc in f.CorrectCases:
                    dfCases.at[caseIndex, "Type"] = f.UnitType.name
                    dfCases.at[caseIndex, "Name"] = f.Name
                    dfCases.at[caseIndex, "Case"] = "CC-> " + cc
                    passed:bool = exp.Unit.RunTest(generated, cc)
                    dfCases.at[caseIndex, "Passed"] = "OK" if passed else "X"
                    dfCases.at[caseIndex, "Generated Code"] = FormatHelper.ShortenCode(generated, 20) if formatCode else generated
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
                    dfCases.at[caseIndex, "Generated Code"] = FormatHelper.ShortenCode(generated, 20) if formatCode else generated
                    if (passed):
                        passedCaseCount = passedCaseCount + 1
                        icPassed = icPassed + 1
                    dfCases.at[caseIndex, "Desc"] = f.Description
                    totalCaseCount = totalCaseCount + 1
                    icCount = icCount + 1
                    caseIndex += 1
                fieldIndex += 1
                #endregion

            model_end_time = time.time()
            model_elapsed_time = model_end_time - model_start_time
            print(f"\tExperiment for model {modelConf} is completed in {self.format_time(model_elapsed_time)} seconds.", )
            modelResults[modelConf] = dfCases

            modelConf:str = model.ConfigKey()
            accuracyColName = f"{modelConf} (%)"
            if(ccCount + icCount + len(f.Conditions) == 0): raise Exception("No cases defined in the dataset!")
            ccAccuracy: float = (float(ccPassed) / float(ccCount)) * 100
            dfAggr.at["CorrectCase", accuracyColName] = ccAccuracy

            #icAccuracy: float = (float(icPassed) / float(icCount)) * 100
            #dfAggr.at["IncorrectCase", accuracyColName] = icAccuracy

            overallAccuracy: float = (float(passedCaseCount) / float(totalCaseCount)) * 100
            dfAggr.at["Overall", accuracyColName] = overallAccuracy

            # precision: float = (float(ccPassed) / float(ccPassed + (icCount - icPassed))) * 100
            # dfAggr.at["Precision", accuracyColName] = precision
            #
            # recall: float = (float(ccPassed) / float(ccCount)) * 100
            # dfAggr.at["Recall", accuracyColName] = recall
            #
            # f1Score: float = 2*precision*recall / (precision + recall)
            # dfAggr.at["F1 Score", accuracyColName] = f1Score
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

if __name__ == '__main__':
    #path = Paths().GetDataset("AtomicDataset-1")
    #ds: Dataset = DatasetXmlRepository.Load(path)

    #HACK (TODO:)
    ds:Dataset = Dataset("SQL")
    ds.Units = []

    #Sample1
    selectUnit:Unit = Unit("SelectQuery","Select all fields from products",UnitType.SQLSelect,None,None)
    selectUnit.Conditions = [
        Condition(Criteria("data-count", "2")),
    ]
    ds.Units.append(selectUnit)

    #Sample2
    selectUnit2: Unit = Unit("SelectQuery2", "Select all products those names are beginning with A letter", UnitType.SQLSelect, None, None)
    selectUnit2.Conditions = [
        Condition(Criteria("data-count", "1")),
    ]
    ds.Units.append(selectUnit2)

    # unit.Conditions.append()
    # unit.Conditions.append()
    # unit.Conditions.append(Criteria("has-column", "ID"))
    # unit.Conditions.append(Criteria("has-column", "Name"))
    # unit.Conditions.append(Criteria("first-record-id", "1"))     #id == unique_key
    # unit.Conditions.append(Criteria("has-record-with-id", "1"))  # id == unique_key

    #exp: Experiment = ExperimentFactory.CreateSingleModelExperiment (UnitType.RegexVal,"ollama","codellama:7b")
    exp = ExperimentFactory().CreateProviderExperiment(UnitType.SQLSelect,"ollama")
    modelFactory = ModelFactory()
    fakeModels = [
        modelFactory.CreateByCfg(ModelConf("Stub")),
    ]
    exp.Models = fakeModels # exp.Models + fakeModels

    exp.Models.append(OllamaModelProvider('codellama'))

    #exp: Experiment = ExperimentFactory.CreateExperimentWithAllModels(UnitType.RegexVal)

    #region Stub Model
    # customize stub
    stubModel = [item for item in exp.Models if item.ModelName().__contains__("Stub")][0]
    fixedRegex: str = r"""^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$"""
    stubModel.StubUnit = fixedRegex  # type: ignore
    stubModel.StubName = "EmailStub"

    #HACK
    stubModel.StubUnit = "select * from Products"
    stubModel.StubName = "SQLStub"
    #endregion

    r:ExperimentResults = ExperimentHost().Run(exp, ds, formatCode=False)
    r.Print()
    ds.Print()