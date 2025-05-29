from langunits.LangUnit import LangUnit, UnitType, EvalRequest, EvalResponse
import re


class StringTransformerPython(LangUnit):
    def __init__(self) -> None:
        super().__init__()

    def PromptText(self):
        return "string transformer method in python"

    def GetUnitType(self) -> UnitType:
        return UnitType.Expression

    def run_test(self, req: EvalRequest) -> EvalResponse:
        passed: bool = self.validate_result(
            req.generated, req.correct_case, req.unit.Context.Data
        )
        return EvalResponse(passed=passed)

    @staticmethod
    def validate_result(generated_code, test_string, input_string) -> bool:
        # Extract the function name using regular expression
        match = re.search(r"def (\w+)\(", generated_code)
        if match:
            function_name = match.group(1)
        else:
            print("Function name could not be determined from the generated code.")
            return False

        # Execute the generated code
        try:
            exec(generated_code)
        except Exception as e:
            print(e)
            return False

        try:
            # Call the dynamically defined function
            if function_name in locals():
                output_string = locals()[function_name](input_string)
                print("input:\t", input_string, "\noutput:\t", output_string)
                return output_string == test_string
            else:
                print(f"Function {function_name} is not defined.")
                return False
        except Exception as e:
            print(e, "\nError while executing the generated code.")
            return False
