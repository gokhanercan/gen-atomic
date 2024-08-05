import os
from openai import OpenAI

from langunits.LangUnit import LangUnitInfo
from models.ModelBase import ModelBase
from colorama import init, Fore, Back, Style
from data.Dataset import *
from models.providers.ModelProviderBase import ModelProviderBase


class ChatGPTModelProvider(ModelProviderBase):

    def __init__(self, activeModelName:str = None) -> None:
        super().__init__()
        ModelBase.__init__(self)
        ModelProviderBase.__init__(self, activeModelName)

    def ProviderName(self):
        return "chatgpt"
    def ProviderAbbreviation(self):
        return "cg"

    @staticmethod
    def ModelNameList()->List[str]:
        return ["gpt-3.5-turbo"]  # cost: <= 1 cent
        #return ["gpt-4"] #cost: approximately 10 cents
    def ModelNames(self):
        return ChatGPTModelProvider.ModelNameList()

    def Generate2(self, finalPrompt: str, langDesc: str) -> str:
        pass

    def Generate(self, description: str, langUnitInfo:LangUnitInfo) -> str:
        openai_api_key = os.getenv('OPEN_AI_API_KEY')
        if not openai_api_key:
            raise ValueError("The OPEN_AI_API_KEY environment variable is not set.")
        client = OpenAI(api_key=openai_api_key)

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

        answer = chat_completion.choices[0].message.content    #phi3,llama2,llama3,deepseek-coder,codegemma,starcoder2  ref:https://ollama.com/library?sort=popular

        gencode:str = str(answer).strip().replace("Regex: ","").replace("```","").replace("`","")      #TODO: Output parsers here please!
        print(f"A: {Fore.CYAN}{gencode}{Fore.RESET}")
        return gencode

if __name__ == "__main__":
    answer = ChatGPTModelProvider('gpt-3.5-turbo').Generate("Generic email address", LangUnitInfo("RegexVal","regular expression for validation"))
    print(answer)