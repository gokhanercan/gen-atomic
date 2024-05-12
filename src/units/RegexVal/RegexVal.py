from colorama import Fore

from units.UnitBase import UnitBase
import re


class RegexVal(UnitBase):

    def __init__(self, unitType) -> None:
        UnitBase.__init__(self,unitType)

    def CheckSyntax(self, code: str):
        pass

    def RunTest(self, code:str, correctCase:str)->bool:
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
