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

        #EXPERIMENT <MODELCONFIG | DATASET>
        #MODELCONFIG <PROVIDER | MODEL | FLOW | PROMPT>
        #MODEL CONF: Exp4029-MFTSG#12-win5-dim100-ns5-hs0-del0-mean1-iter2-root0-inf0-seg3-lang=tr-ngr[no]__TRCorpora2LCNPS2SH-TR2022_MM_NLPTPPRJ1_der0comp0frg0st2.vec
        #ModelProvider[p1:p2]-Model[p1:p2]--Flow[p1:p2]--Prompt[p1:p2]
        #Ollama-codellama:7b -noflow-p1
        #Ollama-codellama:70b-noflow-p1
        #Ollama-phi3:7b-noflow-p1
        #Ollama-phi3:7b-simple:r3-p1

    def ProviderName(self):
        return "chatgpt"

    def ProviderAbbreviation(self):
        return "cg"

    def ModelName(self):
        return self.ModelConfiguration

    @staticmethod
    def ModelConfigurationsList()->List[str]:
        return ["gpt-3.5-turbo"]  # cost: <= 1 cent
        #return ["gpt-4"] #cost: approximately 6 cents
    def ModelConfigurations(self):
        return ChatGPTModelProvider.ModelConfigurationsList()

    def Generate(self, description: str) -> str:

        modelName = self.ModelConfiguration

        client = OpenAI(
            # This is the default and can be omitted
            api_key="sk-gen-atomic-key-XhFAbEnBiGODTwE3IgX6T3BlbkFJJabbjULa8lJaflR5Fpfs",
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