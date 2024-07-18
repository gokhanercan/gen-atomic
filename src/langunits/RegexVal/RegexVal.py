from colorama import Fore
from data.Dataset import Unit
from langunits.LangUnit import LangUnit, UnitType
import re


class RegexVal(LangUnit):
    def __init__(self) -> None:
        super().__init__()

    def PromptText(self):
        return "regular expression for validation"
    def GetUnitType(self) -> UnitType:
        return UnitType.Expression
    def CheckSyntax(self, code: str):
        pass

    def RunTest(self, code:str, correctCase:str, unit:Unit)->bool:
        return self.validate_regex(code, correctCase)

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
        # except re.error:
        except:
            print(f"{Fore.RED}Invalid regular expression pattern.{Fore.RESET}")  # TODO: Handle that error well. Reflection.
            return False
    # endregion
