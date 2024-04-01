
# pip install langchain
from abc import ABC, abstractmethod
import re



class IRegexGenerator(ABC): #TODO:Rename it to Provider     #This should become a lang provider. So validate/compile/syntax chgecking etc. should be provided from langprovider.

    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def Generate(self, description:str)->str:   #desc: price for TK
        pass


class StubRegexGenerator(IRegexGenerator):
    def __init__(self, regex:str) -> None:
        super().__init__()
        self.Regex = regex

    def Generate(self, description: str) -> str:
        return self.Regex

class RegexHost(object):        #TODO: Load ds here.

    def __init__(self, regexGen:IRegexGenerator) -> None:
        super().__init__()
        self.RegexGen:IRegexGenerator = regexGen

    def Run(self, fields):
        # TODO: df here.
        passedCaseCount:int = 0
        totalCaseCount: int = 0
        for f in fields:
            generated:str = self.RegexGen.Generate(f.Description)
            for cc in f.CorrectCases:
                passed:bool = RegexHost.validate_regex(generated,cc)
                if(passed): passedCaseCount = passedCaseCount + 1
                totalCaseCount = totalCaseCount + 1
                if(passed):
                    print("[Passed] Field '" + str(f) + "':" + "with regex '" + generated + "' for correct case " + cc)
                else:
                    print("[Failed] Field '" + str(f) + "':" + "with regex '" + generated + "' for correct case " + cc)
            #TODO: Incorrect cases

        print("Overall accuracy:" + str((float(passedCaseCount) / float(totalCaseCount)) * 100))

    @staticmethod
    def validate_regex(regex_pattern, test_string)->bool:
        try:
            compiled_pattern = re.compile(regex_pattern)
            match = compiled_pattern.search(test_string)
            if match:
                print("Regex is valid and matches the test string.")
                return True
            else:
                print("Regex is valid but does not match the test string.")
                return False
        except re.error:
            print("Invalid regular expression pattern.")
            return False

if __name__ == '__main__':
    # from ds

    fixedRegex:str = """^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$"""
    RegexHost(StubRegexGenerator(fixedRegex)).Run(fields)