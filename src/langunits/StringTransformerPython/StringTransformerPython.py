from data.Dataset import Unit
from langunits.LangUnit import LangUnit, UnitType
import re


class StringTransformerPython(LangUnit):
    def __init__(self) -> None:
        super().__init__()

    def PromptText(self):
        return "string transformer method in python"
    def GetUnitType(self) -> UnitType:
        return UnitType.Expression
    def CheckSyntax(self, code: str):
        pass

    def RunTest(self, code:str, correctCase:str, unit:Unit)->bool:
        return self.validate_result(code, correctCase, unit.Context.Data)

    @staticmethod
    def validate_result(generated_code, test_string, input_string) -> bool:

        # Extract the function name using regular expression
        match = re.search(r'def (\w+)\(', generated_code)
        if match:
            function_name = match.group(1)
        else:
            raise ValueError("Function name could not be determined from the generated code.")

        # Execute the generated code
        exec(generated_code)

        try:
            # Call the dynamically defined function
            if function_name in locals():
                output_string = locals()[function_name](input_string)
                print("input:\t", input_string, "\noutput:\t", output_string)
                return output_string == test_string
            else:
                print(f"Function {function_name} is not defined.")
                return False
        except:
            raise Exception("Error while executing the generated code.")
