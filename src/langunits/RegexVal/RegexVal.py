from colorama import Fore
from data.Dataset import Unit
from langunits.LangUnit import LangUnit, UnitType, EvalRequest, EvalResponse
import re

# from models.ModelBase import EvalResponse, GenResponse, EvalRequest


class RegexVal(LangUnit):
    def __init__(self) -> None:
        super().__init__()

    def PromptText(self):
        return "regular expression for validation"

    def GetUnitType(self) -> UnitType:
        return UnitType.Expression

    def CheckSyntax(self, code: str):
        pass

    def RunTest(self, code:str, correctCase:str, unit:Unit)->bool:      #TODO: unit is not used. Remove it.
        #TODO: Eval multiple test cases in a single call by accepting dataset unit(field).
        return self.validate_regex(code, correctCase)

    def run_test(self, eval_req:EvalRequest)->EvalResponse:
        passed:bool =  self.validate_regex(eval_req.generated, eval_req.correct_case)
        return EvalResponse(passed)

    # region Regex Implementation
    @staticmethod
    def validate_regex(regex_pattern, test_string) -> bool:
        try:
            compiled_pattern = re.compile(regex_pattern)
            match = compiled_pattern.search(test_string)
            if match:
                return True
            else:
                return False
        except:
            print(f"{Fore.RED}Invalid regular expression pattern.{Fore.RESET}")  # TODO: Handle that error well. Reflection.
            return False
    # endregion
