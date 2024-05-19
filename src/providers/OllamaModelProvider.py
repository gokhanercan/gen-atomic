import time
from typing import List

from models.ModelBase import ModelBase
import subprocess
import ollama
from colorama import init, Fore, Back, Style

from providers.ModelProviderBase import ModelProviderBase


class OllamaModelProvider(ModelProviderBase, ModelBase):

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
        return "ollama"

    def ProviderAbbreviation(self):
        return "ol"

    def ModelName(self):
        return self.ModelConfiguration

    @staticmethod
    def ModelConfigurationsList()->List[str]:
        #return ["codellama", "phi3"]
        return ["codellama","llama3","phi3","codegemma","codellama:70b","llama3:70b","starcoder2","gemma","tinyllama"]
        #return ["codellama", "codellama:70b", "phi3", "llama3:7b", "llama2"]  # ? :
    def ModelConfigurations(self):
        return OllamaModelProvider.ModelConfigurationsList()

    def start_ollama_server(self):
        """
        #client examples: https://github.com/ollama/ollama-python/tree/main/examples
        # Use WSL command to launch Ollama on localhost (accessible from Windows)
        # For Win, Set env variable OLLAMA_MODELS for root models dir ref:https://github.com/ollama/ollama/blob/main/docs/faq.md#where-are-models-stored
        :return:
        """
        modelName = self.ModelConfiguration
        process = subprocess.Popen(["ollama run", modelName], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        process.communicate()
        return process

    def Generate(self, description: str) -> str:

        modelName = self.ModelConfiguration
        #ollama_server_process = self.start_ollama_server()

        client = ollama.Client('http://localhost:11434')  # Specify full URL with port
        instruction:str = "Consider yourself a function that takes the input of asked validation regex statement, and your output is '''Regex: {created regex}''' Do not give me an explanation, only give me a regex expression. Do not add any additional characters."
        prompt:str = f"{instruction}\nAsked regex statement: {description}."
        promptColored: str = f"{instruction}\nAsked regex statement: {Fore.BLUE}{description}{Fore.RESET}."
        print(f"\nP:{promptColored}")
        print(Fore.RESET)
        response = client.generate(model=modelName, prompt=prompt)        #phi3,llama2,llama3,deepseek-coder,codegemma,starcoder2  ref:https://ollama.com/library?sort=popular
        answer = response['response']

        #ollama_server_process.terminate()       #TODO: Manage the connecion. Do not terminate on every call.

        gencode:str = str(answer).strip().replace("Regex: ","").replace("```","").replace("`","")      #TODO: Output parsers here please!
        print(f"A: {Fore.CYAN}{gencode}{Fore.RESET}")
        return gencode

if __name__ == "__main__":
    answer = OllamaModelProvider('codellama:7b').Generate("generate me an email regex, do not give me an explanation")
    print(answer)