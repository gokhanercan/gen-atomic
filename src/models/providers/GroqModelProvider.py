import os
from groq import Groq

from langunits.LangUnit import LangUnitInfo
from models.ModelBase import ModelBase
from colorama import init, Fore, Back, Style
from data.Dataset import *
from models.providers.ModelProviderBase import ModelProviderBase


class GroqModelProvider(ModelProviderBase):

    def __init__(self, activeModelName:str = None) -> None:
        super().__init__()
        ModelBase.__init__(self)
        ModelProviderBase.__init__(self, activeModelName)

    def ProviderName(self):
        return "groq"

    def ProviderAbbreviation(self):
        return "gr"

    @staticmethod
    def ModelNameList()->List[str]:
        return ["llama-3.1-70b-versatile", "llama3-70b-8192"]  # cost: <= 1 cent
    #all available models:
    # gemma2-9b-it, gemma-7b-it, llama-3.1-70b-versatile, llama-3.1-8b-instant, llama3-70b-8192, llama3-8b-8192,
    # llama3-groq-70b-8192-tool-use-preview, llama3-groq-8b-8192-tool-use-preview, mixtral-8x7b-32768, whisper-large-v3

    def ModelNames(self):
        return GroqModelProvider.ModelNameList()

    def Generate(self, description: str, langUnitInfo:LangUnitInfo) -> str:
        groq_api_key = os.environ.get("GROQ_API_KEY")
        if not groq_api_key:
            raise ValueError("The GROQ_API_KEY environment variable is not set.")
        client = Groq(api_key=groq_api_key)

        instruction:str = "Consider yourself a function that takes the input of asked validation regex statement, and your output is '''Regex: {created regex}''' Do not give me an explanation, only give me a regex expression. Do not add any additional characters."
        prompt:str = f"\nAsked regex statement: {description}."
        promptColored: str = f"{instruction}\nAsked regex statement: {Fore.BLUE}{description}{Fore.RESET}."
        print(f"\nP:{promptColored}")
        print(Fore.RESET)

        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": instruction
                 },
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model=self.ModelName(),
        )

        answer = chat_completion.choices[0].message.content

        gencode:str = str(answer).strip().replace("Regex: ","").replace("```","").replace("`","")      #TODO: Output parsers here please!
        print(f"A: {Fore.CYAN}{gencode}{Fore.RESET}")
        return gencode

if __name__ == "__main__":
    answer = GroqModelProvider('llama-3.1-70b-versatile').Generate("Generic email address", LangUnitInfo("RegexVal","regular expression for validation"))
    print(answer)