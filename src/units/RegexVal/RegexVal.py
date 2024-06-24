from colorama import Fore

from units.UnitBase import UnitBase
import re


class RegexVal(UnitBase):

    def __init__(self, unitType) -> None:
        UnitBase.__init__(self,unitType)

    # def GetUnitType(self):
    #     return "Expression"     #Function|Class|Module....

    def CheckSyntax(self, code: str):
        pass

    def RunTest(self, code:str, correctCase:str)->bool:
        return self.validate_regex(code, correctCase)

    def getPrompt(self, description) -> str:
        instruction: str = (
            "Consider yourself a function that takes the input of asked validation regex statement, and "
            "your output should be a markdown code snippet formatted in the following schema, including "
            "the leading and trailing \"```regex\" and \"```\". Do not give me an explanation, only give "
            "me a regex expression. Do not add any additional characters.")
        prompt: str = f"{instruction}\nAsked regex statement: {description}."
        promptColored: str = f"{instruction}\nAsked regex statement: {Fore.BLUE}{description}{Fore.RESET}."
        print(f"\nP:{promptColored}")
        print(Fore.RESET)

        return prompt
    # region Regex Implementation

    def parseOutput(self, answer) -> str:
        regex_pattern = r"```regex(.*?)```"
        match = re.search(regex_pattern, answer, re.DOTALL)  # re.DOTALL allows matching newlines

        print(f"Full Output:\n{answer}\n")

        if match:

            extracted_regex = match.group(1)
            print(f"Extracted regex pattern: {Fore.CYAN}{extracted_regex}{Fore.RESET}")
            return extracted_regex.strip()
        else:
            print("Couldn't find regex pattern between ```")
            return answer

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

