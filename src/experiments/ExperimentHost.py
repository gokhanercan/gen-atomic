import time
from typing import Optional, List, Dict

from data.Dataset import Dataset, Unit, Criteria, Constraint
from data.DatasetXmlRepository import DatasetXmlRepository
from experiments.Experiment import Experiment, ExperimentFactory
from pandas import DataFrame  # type: ignore
from tabulate import tabulate  # type: ignore

from experiments.ModelConfiguration import ModelConfigurations
from langunits.LangUnit import LangUnitInfo, EvalRequest, LangUnit
from langunits.LangUnitFactory import LangUnitFactory
from models.ModelBase import GenResponse, GenRequest
from models.ModelFactory import ModelFactory, ModelFilters
from models.StubModel import StubModel
from prompting.prompting_factory import PromptingFactory
from prompting.repo.inmemory_prompt_repository import InMemoryPromptRepository
from prompting.repo.prompt_repository_base import PromptRepositoryBase
from utility.FormatHelper import FormatHelper
from utility.Paths import Paths


class ExperimentResults(object):

    def __init__(self, experiment_name: str, experiment_key: str, **kwargs) -> None:
        super().__init__()
        self.experiment_name: str = experiment_name
        self.experiment_key: str = experiment_key
        self.model_results: Dict[str, DataFrame] = {}
        self.results: DataFrame = Optional[DataFrame]
        self.overall_accuracy: List = Optional[List]
        self.model_keys: List = Optional[List]
        for key, value in kwargs.items():
            setattr(self, key, value)

    def print(self, ignore_fake_model_reports=True):
        if self.model_results is not None:
            fake_model_names = ModelFactory().get_all_baseline_model_names()
            for model_conf, df in self.model_results.items():
                if ignore_fake_model_reports:
                    if fake_model_names.__contains__(model_conf):
                        continue
                    if model_conf.__contains__("Stub"):
                        continue
                    if model_conf.__contains__("Random"):
                        continue
                print(f"\n-- {model_conf.upper()} MODEL RESULTS --")
                # region styling
                # for index, row in df.iterrows():
                #     if row['Passed'] == "OK":
                #         df.at[index, 'Passed'] = f"{Fore.GREEN}OK{Fore.RESET}"
                #         df.at[index, 'Case'] = f"{Fore.GREEN}{row['Case']}{Fore.RESET}"
                #     if row['Passed'] == "X":
                #         df.at[index, 'Passed'] = f"{Fore.RED}X{Fore.RESET}"
                #         df.at[index, 'Case'] = f"{Fore.RED}{row['Case']}{Fore.RESET}"
                # endregion
                print(tabulate(df, headers="keys", tablefmt="grid", floatfmt=".2f"))
        if self.results is not None:
            experiment_header = f"-- {self.experiment_name.upper()} EXPERIMENT --"
            print("\n" + experiment_header)
            print(tabulate(self.results, headers="keys", tablefmt="psql", floatfmt=".2f"))
            print(f"{self.experiment_key}")
        if self.model_keys:
            print(f"\n-- MODEL KEYS --")
            print(tabulate(self.model_keys, headers=[], tablefmt="psql", floatfmt=".2f"))


class ExperimentHost(object):

    def run(self, exp: Experiment, ds: Dataset, format_code: bool = False):
        if exp.model_configs.__len__() == 0:
            raise Exception("No model configuration(s) defined in the experiment!")
        start_time = time.time()
        print(
            f"\nRunning experiment on {ds.name} dataset with {str(len(exp.model_configs))} model configuration(s) ..."
        )
        print("ModelConfigs:", exp.model_configs)

        model_results: Dict[str, DataFrame] = {}

        df_aggr = DataFrame()
        for mc in exp.model_configs.model_configs:
            model_start_time = time.time()
            model = mc.model
            print(f"\tRunning model config '{mc.key()} on '{ds.name}' dataset ...")
            df_cases: DataFrame = DataFrame()
            field_index: int = 1
            case_index: int = 1
            passed_case_count: int = 0
            total_case_count: int = 0
            cc_count: int = 0
            ic_count: int = 0
            cc_passed: int = 0
            ic_passed: int = 0

            y_true: List[int] = []
            y_pred: List[int] = []

            for f in ds.units:
                lang_unit_info: LangUnitInfo = exp.lang_unit.create_info()

                # gen2
                res: GenResponse = mc.prompting._generate(
                    GenRequest(
                        lang_unit_info=lang_unit_info,
                        description=f.description,
                        gen_model=model,
                        final_prompt=None,
                    )
                )
                generated: str = res.raw_generated
                passed: bool = True

                # region Eval Constraints
                # exp.lang_unit.run_test(EvalRequest(generated,"",f,lang_unit_info)).passed
                # generated: str = model.Generate(f.description, lang_unit_info)
                # passed: bool = exp.lang_unit.RunTest(generated, "",f) # TODO: Duplicate RunTest on Constraint and CCase/ICCase.

                df_cases.at[case_index, "Type"] = f.unit_type
                df_cases.at[case_index, "Name"] = f.name
                df_cases.at[case_index, "Passed"] = "OK" if passed else "X"
                df_cases.at[case_index, "Generated Code"] = (
                    FormatHelper.ShortenCode(generated, 20) if format_code else generated
                )
                if passed:
                    passed_case_count = passed_case_count + 1
                    cc_passed = cc_passed + 1
                df_cases.at[case_index, "Desc"] = f.description
                total_case_count = total_case_count + 1
                cc_count = cc_count + 1
                case_index += 1

                y_true.append(1)
                y_pred.append(int(passed))
                # endregion

                # region Cases
                for cc in f.correct_cases:
                    df_cases.at[case_index, "Type"] = f.unit_type
                    df_cases.at[case_index, "Name"] = f.name
                    df_cases.at[case_index, "Case"] = "CC-> " + cc
                    passed: bool = exp.lang_unit.run_test(EvalRequest(generated, cc, f, lang_unit_info)).passed
                    df_cases.at[case_index, "Passed"] = "OK" if passed else "X"
                    df_cases.at[case_index, "Generated Code"] = (
                        FormatHelper.ShortenCode(generated, 20) if format_code else generated
                    )
                    if passed:
                        passed_case_count = passed_case_count + 1
                        cc_passed = cc_passed + 1
                    df_cases.at[case_index, "Desc"] = f.description
                    total_case_count = total_case_count + 1
                    cc_count = cc_count + 1
                    case_index += 1
                    y_true.append(1)
                    y_pred.append(int(passed))

                for icc in f.incorrect_cases:
                    df_cases.at[case_index, "Type"] = f.unit_type
                    df_cases.at[case_index, "Name"] = f.name
                    df_cases.at[case_index, "Case"] = "IC-> " + icc
                    passed: bool = not exp.lang_unit.run_test(EvalRequest(generated, icc, f, lang_unit_info)).passed  # type: ignore
                    df_cases.at[case_index, "Passed"] = "OK" if passed else "X"
                    df_cases.at[case_index, "Generated Code"] = (
                        FormatHelper.ShortenCode(generated, 20) if format_code else generated
                    )
                    if passed:
                        passed_case_count = passed_case_count + 1
                        ic_passed = ic_passed + 1
                    df_cases.at[case_index, "Desc"] = f.description
                    total_case_count = total_case_count + 1
                    ic_count = ic_count + 1
                    case_index += 1
                    y_true.append(0)
                    y_pred.append(int(not passed))
                field_index += 1
                # endregion

            model_end_time = time.time()
            model_elapsed_time = model_end_time - model_start_time
            print(
                f"\tExperiment for mc {mc.key()} is completed in {self.format_time(model_elapsed_time)} seconds.",
            )
            model_results[model.key()] = df_cases

            accuracy_col_name = f"{mc.key()} (%)"
            # if(cc_count + ic_count + len(f.Conditions) == 0): raise Exception("No cases defined in the dataset!") TODO: commented because of a lack of Conditions implementation
            cc_accuracy: float = (float(cc_passed) / float(cc_count)) * 100 if cc_count > 0 else 0
            df_aggr.at["CorrectCase", accuracy_col_name] = cc_accuracy

            overall_accuracy: float = (float(passed_case_count) / float(total_case_count)) * 100 if total_case_count > 0 else 0
            df_aggr.at["Overall", accuracy_col_name] = overall_accuracy

            # region Precision, Recall, F1 Score
            from sklearn.metrics import precision_score, recall_score, f1_score

            # Calculate precision, recall, and F1-score
            df_aggr.at["Precision", accuracy_col_name] = precision_score(y_true, y_pred, zero_division=0) * 100
            df_aggr.at["Recall", accuracy_col_name] = recall_score(y_true, y_pred, zero_division=0) * 100
            df_aggr.at["F1 Score", accuracy_col_name] = f1_score(y_true, y_pred, zero_division=0) * 100
            # endregion

        end_time = time.time()
        elapsed_time = end_time - start_time
        print(
            f"Experiment is completed in {self.format_time(elapsed_time)} seconds.",
        )

        overall_accuracy: List = df_aggr.iloc[-1]
        r = ExperimentResults(exp.plain_name(), exp.key(), overall_accuracy=overall_accuracy)
        r.model_results = model_results
        r.results = df_aggr
        r.model_keys = [[mc.key()] for mc in exp.model_configs.model_configs]
        return r

    def format_time(self, seconds):
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return "{:02}:{:02}:{:02}".format(int(hours), int(minutes), int(seconds))


def _prompt_repo() -> PromptRepositoryBase:
    return InMemoryPromptRepository()


# region Sample Experiments
def RunSQLSelectExperiment():
    path = Paths().GetDataset("AtomicSQLSelectDataset")
    ds: Dataset = DatasetXmlRepository.load(path)

    exp = ExperimentFactory("SqlSelect", _prompt_repo()).create_experiment_by_model_filters(
        ModelFilters(providerAbbr="ol", keyContains="codellama"),
        include_baselines=False,
    )

    r: ExperimentResults = ExperimentHost().run(exp, ds, format_code=False)
    r.print()
    ds.print()


def RunRegexValExperiment():
    # Dataset
    path = Paths().GetDataset("AtomicRegexValDataset")
    ds: Dataset = DatasetXmlRepository.load(path)

    # Exp. Context
    exp_factory = ExperimentFactory("RegexVal", _prompt_repo(), PromptingFactory().create_default("RegexVal"))
    exp: Experiment = exp_factory.create_single_model_experiment("np.stub")

    stubs = [item for item in exp.get_models() if isinstance(item, StubModel)]
    StubModel.fake_email(stubs)

    r: ExperimentResults = ExperimentHost().run(exp, ds, format_code=True)
    r.print()
    # ds.print()


def RunStringTransformerPythonExperiment():
    path = Paths().GetDataset("AtomicStringTransformerPythonDataset")
    ds: Dataset = DatasetXmlRepository.load(path)

    exp = ExperimentFactory("StringTransformerPython", _prompt_repo()).create_experiment_by_model_filters(
        ModelFilters(keyContains="llama3"), include_baselines=False
    )

    r: ExperimentResults = ExperimentHost().run(exp, ds, format_code=True)
    r.print()


def run_model_experiment_comparing_prompts(
    lang_unit_name: str = "RegexVal",
    ds_name: str = "AtomicRegexValDataset",
    model_key: str = "np.stub",
):
    path = Paths().GetDataset(ds_name)
    ds: Dataset = DatasetXmlRepository.load(path)
    ds.units = ds.units[:1]
    exp_factory = ExperimentFactory(lang_unit_name, _prompt_repo())
    exp: Experiment = exp_factory.create_model_experiment_with_all_default_promptings(model_key, True)
    stubs = [item for item in exp.get_models() if isinstance(item, StubModel)]
    StubModel.fake_email(stubs)

    r: ExperimentResults = ExperimentHost().run(exp, ds, format_code=True)
    print(exp)
    r.print()


def run_manually_defined_experiment():
    path = Paths().GetDataset("AtomicRegexValDataset")
    ds: Dataset = DatasetXmlRepository.load(path)
    lang_unit_name: str = "RegexVal"
    lang_unit: LangUnit = LangUnitFactory().create(lang_unit_name)
    exp_factory: ExperimentFactory = ExperimentFactory(lang_unit_name, _prompt_repo())
    model_key: str = "np.stub"
    exp = exp_factory.create_single_model_experiment(
        model_key, PromptingFactory(_prompt_repo()).create_default(lang_unit_name)
    )
    mcs = ModelConfigurations(
        []
        + exp_factory.create_model_configurations_with_all_default_promptings(model_key, True)
        # + exp_factory.create_model_configurations_with_all_default_promptings("np.random", True)
    )
    exp: Experiment = Experiment(lang_unit, mcs)
    stubs = [item for item in exp.get_models() if isinstance(item, StubModel)]
    StubModel.fake_email(stubs)

    r: ExperimentResults = ExperimentHost().run(exp, ds, format_code=True)
    r.print()


# endregion


if __name__ == "__main__":
    # run_manually_defined_experiment()
    run_model_experiment_comparing_prompts("RegexVal", "AtomicRegexValDataset", "ol.llama3:latest")
    # run_model_experiment_comparing_prompts("RegexVal", "AtomicRegexValDataset", "np.stub")
    # RunSQLSelectExperiment()
    # RunRegexValExperiment()
    # RunStringTransformerPythonExperiment()
