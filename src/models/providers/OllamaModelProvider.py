from typing import List
import re

from langunits.LangUnit import LangUnitInfo
from models.ModelBase import ModelBase
import subprocess
import ollama
from colorama import init, Fore, Back, Style
from data.Dataset import *
from models.providers.ModelProviderBase import ModelProviderBase

class OllamaModelProvider(ModelProviderBase):
    def __init__(self, activeModelName:str = None) -> None:
        super().__init__()
        ModelBase.__init__(self)
        ModelProviderBase.__init__(self, activeModelName)

        #region Naming convention ideas
        #EXPERIMENT <MODELCONFIG | DATASET>
        #MODELCONFIG <PROVIDER | MODEL | FLOW | PROMPT>
        #MODEL CONF: Exp4029-MFTSG#12-win5-dim100-ns5-hs0-del0-mean1-iter2-root0-inf0-seg3-lang=tr-ngr[no]__TRCorpora2LCNPS2SH-TR2022_MM_NLPTPPRJ1_der0comp0frg0st2.vec
        #ModelProvider[p1:p2]-Model[p1:p2]--Flow[p1:p2]--Prompt[p1:p2]
        #Ollama-codellama:7b -noflow-p1
        #Ollama-codellama:70b-noflow-p1
        #Ollama-phi3:7b-noflow-p1
        #Ollama-phi3:7b-simple:r3-p1
        #endregion
    def ProviderName(self):
        return "ollama"
    def ProviderAbbreviation(self):
        return "ol"

    @staticmethod
    def ModelNameList()->List[str]:       #str:ModelNames
        return ["codellama","llama3"]
        #TODO: Dynamically fetch list of models supported by Ollama. After implementing this drop static support and self.ModelConfigurations signature.
        #return ["codellama","llama3","phi3","codegemma","codellama:70b","llama3:70b","starcoder2","gemma","tinyllama"]
        #return ["codellama", "codellama:70b", "phi3", "llama3:7b", "llama2"]  # ? :
    def ModelNames(self):   #str:ModelNames
        return OllamaModelProvider.ModelNameList()

    def start_ollama_server(self):
        """
        #client examples: https://github.com/ollama/ollama-python/tree/main/examples
        # Use WSL command to launch Ollama on localhost (accessible from Windows)
        # For Win, Set env variable OLLAMA_MODELS for root models dir ref:https://github.com/ollama/ollama/blob/main/docs/faq.md#where-are-models-stored
        :return:
        """
        process = subprocess.Popen(["ollama run", self.ModelName()], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        process.communicate()
        return process

    def Generate(self, description: str, langUnitInfo:LangUnitInfo) -> str:
        """
        TODO: https://github.com/users/gokhanercan/projects/3/views/1?pane=issue&itemId=71867358
        :param description:
        :param langUnitInfo:
        :return:
        """
        #ollama_server_process = self.start_ollama_server()
        client = ollama.Client('http://localhost:11434')  # Specify full URL with port

        #prompt
        langDesc:str = langUnitInfo.PromptText
        instruction: str = (f"Consider yourself a function that takes the input of asked validation {langDesc} statement, and "
                            f"your output should be a markdown code snippet formatted in the following schema, including "
                            f"the leading and trailing \"```{langDesc}\" and \"```\". Do not give me an explanation, only give "
                            f"me a {langDesc} expression. Do not add any additional characters.")
        prompt: str = f"{instruction}\nAsked {langDesc} statement: {description}."
        promptColored: str = f"{instruction}\nAsked {langDesc} statement: {Fore.BLUE}{description}{Fore.RESET}."
        print(f"\nP:{promptColored}")
        print(Fore.RESET)

        response = client.generate(model=self.ModelName(), prompt=prompt)        #phi3,llama2,llama3,deepseek-coder,codegemma,starcoder2  ref:https://ollama.com/library?sort=popular
        answer = response['response']

        sql_pattern = rf"```{langDesc}(.*?)```"
        match = re.search(sql_pattern, answer, re.DOTALL)  # re.DOTALL allows matching newlines
        print(f"Full Output:\n{answer}\n")

        if match:
            extracted_sql = match.group(1)
            print(f"Extracted {langDesc} pattern: {Fore.CYAN}{extracted_sql}{Fore.RESET}")
            answer = extracted_sql.strip()
        else:
            print(f"Couldn't find {langDesc} pattern between ```")

        #ollama_server_process.terminate()       #TODO: Manage the connection. Do not terminate on every call.

        gencode:str = str(answer).strip().replace("Regex: ","").replace("regexp","").replace("```","").replace("`","").replace("SQL: ","")      #TODO: Output parsers here please!
        print(f"A: {Fore.CYAN}{gencode}{Fore.RESET}")
        return gencode

    def Generate2(self, finalPrompt:str, langDesc:str) -> str:
        #prompt
        # langDesc:str = langUnitInfo.PromptText
        # instruction: str = (f"Consider yourself a function that takes the input of asked validation {langDesc} statement, and "
        #                     f"your output should be a markdown code snippet formatted in the following schema, including "
        #                     f"the leading and trailing \"```{langDesc}\" and \"```\". Do not give me an explanation, only give "
        #                     f"me a {langDesc} expression. Do not add any additional characters.")
        # prompt: str = f"{instruction}\nAsked {langDesc} statement: {description}."
        # promptColored: str = f"{instruction}\nAsked {langDesc} statement: {Fore.BLUE}{description}{Fore.RESET}."
        # print(f"\nP:{promptColored}")
        # print(Fore.RESET)

        client = ollama.Client('http://localhost:11434')  # Specify full URL with port
        response = client.generate(model=self.ModelName(), prompt=finalPrompt)        #phi3,llama2,llama3,deepseek-coder,codegemma,starcoder2  ref:https://ollama.com/library?sort=popular
        answer = response['response']

        #region Parser
        sql_pattern = rf"```{langDesc}(.*?)```"
        match = re.search(sql_pattern, answer, re.DOTALL)  # re.DOTALL allows matching newlines
        print(f"Full Output:\n{answer}\n")
        if match:
            extracted_sql = match.group(1)
            print(f"Extracted {langDesc} pattern: {Fore.CYAN}{extracted_sql}{Fore.RESET}")
            answer = extracted_sql.strip()
        else:
            print(f"Couldn't find {langDesc} pattern between ```")
        #ollama_server_process.terminate()       #TODO: Manage the connection. Do not terminate on every call.

        gencode:str = str(answer).strip().replace("Regex: ","").replace("regexp","").replace("```","").replace("`","").replace("SQL: ","")      #TODO: Output parsers here please!
        print(f"A: {Fore.CYAN}{gencode}{Fore.RESET}")
        #endregion
        return gencode

if __name__ == "__main__":
    answer = OllamaModelProvider('codellama').Generate("generate me an email regex, do not give me an explanation",
                    LangUnitInfo("RegexVal", "regular expression for validation"))
    print(answer)