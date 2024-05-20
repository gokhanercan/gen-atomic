import os
import time
from typing import List
from openai import OpenAI
from models.ModelBase import ModelBase
from colorama import init, Fore, Back, Style
from providers.ModelProviderBase import ModelProviderBase


class ChatGPTModelProvider(ModelProviderBase, ModelBase):

    def __init__(self, modelConfiguration:str) -> None:
        super().__init__()
        ModelBase.__init__(self)
        self.ModelConfiguration = modelConfiguration     #TODO: add to params. model:70b

    def ProviderName(self):
        return "chatgpt"

    def ProviderAbbreviation(self):
        return "cg"

    def ModelName(self):
        return self.ModelConfiguration

    @staticmethod
    def ModelConfigurationsList()->List[str]:
        return ["gpt-3.5-turbo"]  # cost: <= 1 cent
        #return ["gpt-4"] #cost: approximately 10 cents
    def ModelConfigurations(self):
        return ChatGPTModelProvider.ModelConfigurationsList()

    def Generate(self, description: str) -> str:

        modelName = self.ModelConfiguration

        openai_api_key = os.getenv('OPEN_AI_API_KEY')

        if not openai_api_key:
            raise ValueError("The OPEN_AI_API_KEY environment variable is not set.")

        client = OpenAI(
            api_key=openai_api_key,
        )

        instruction:str = "Consider yourself a function that takes the input of asked validation regex statement, and your output is '''Regex: {created regex}''' Do not give me an explanation, only give me a regex expression. Do not add any additional characters."
        prompt:str = f"{instruction}\nAsked regex statement: {description}."
        promptColored: str = f"{instruction}\nAsked regex statement: {Fore.BLUE}{description}{Fore.RESET}."
        print(f"\nP:{promptColored}")
        print(Fore.RESET)

        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model=modelName,
        )

        answer = chat_completion.choices[0].message.content    #phi3,llama2,llama3,deepseek-coder,codegemma,starcoder2  ref:https://ollama.com/library?sort=popular

        gencode:str = str(answer).strip().replace("Regex: ","").replace("```","").replace("`","")      #TODO: Output parsers here please!
        print(f"A: {Fore.CYAN}{gencode}{Fore.RESET}")
        return gencode

if __name__ == "__main__":
    answer = ChatGPTModelProvider('gpt-3.5-turbo').Generate("Generic email address")
    print(answer)