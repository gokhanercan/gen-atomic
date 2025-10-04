import os

from langunits.LangUnit import LangUnitInfo
from models.ModelBase import ModelBase
from colorama import init, Fore, Back, Style
from data.Dataset import *
from models.ModelBase import GenResponse, GenRequest
from models.providers.ModelProviderBase import ModelProviderBase


class GroqModelProvider(ModelProviderBase):

    def __init__(self, active_model_name: str = None) -> None:
        super().__init__()
        ModelBase.__init__(self)
        ModelProviderBase.__init__(self, active_model_name)

    def ProviderName(self):
        return "groq"

    def ProviderAbbreviation(self):
        return "gr"

    def model_names(self) -> list[str]:
        return ["groq"]

    @deprecated
    def Generate(self, description: str, langUnitInfo: LangUnitInfo) -> str:
        from groq import Groq

        groq_api_key = os.environ.get("GROQ_API_KEY")
        if not groq_api_key:
            raise ValueError("The GROQ_API_KEY environment variable is not set.")
        client = Groq(api_key=groq_api_key)

        instruction: str = (
            "Consider yourself a function that generates a string transformer method in python, and your output is '''python: {created python string transformer method}''' Do not give me an explanation, only give me a python method. Do not add any additional characters."
        )
        prompt: str = f"\nAsked python string transformer method: {description}."
        promptColored: str = (
            f"{instruction}\nAsked python string transformer method: {Fore.BLUE}{description}{Fore.RESET}."
        )
        print(f"\nP:{promptColored}")
        print(Fore.RESET)

        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": instruction},
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            model=self.ModelName(),
        )

        answer = chat_completion.choices[0].message.content

        gencode: str = (
            str(answer)
            .strip()
            .replace("Regex: ", "")
            .replace("SQL: ", "")
            .replace("```", "")
            .replace("`", "")
            .replace("python: ", "")
        )  # TODO: Output parsers here please!
        print(f"A: {Fore.CYAN}{gencode}{Fore.RESET}")
        return gencode

    def _generate_impl(self, req: GenRequest) -> GenResponse:
        pass


if __name__ == "__main__":
    answer = GroqModelProvider("llama-3.1-70b-versatile").Generate(
        "Generic email address",
        LangUnitInfo("RegexVal", "regular expression for validation"),
    )
    print(answer)
