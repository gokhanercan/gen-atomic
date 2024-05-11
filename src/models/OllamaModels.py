import time
from models.ModelBase import ModelBase
import subprocess
import ollama


class OllamaModels(ModelBase):

    def __init__(self, modelName:str) -> None:
        super().__init__()
        #self._ModelName = modelName

    def start_ollama_server(self):      #client examples: https://github.com/ollama/ollama-python/tree/main/examples
        # Use WSL command to launch Ollama on localhost (accessible from Windows)

        process = subprocess.Popen(["wsl", "--user", "root", "--", "ollama run", "codellama"], stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE)
        process.communicate()
        return process

    def Generate(self, description: str) -> str:

        ollama_server_process = self.start_ollama_server()
        #time.sleep(2)  # Adjust delay as needed

        client = ollama.Client('http://localhost:11434')  # Specify full URL with port
        instruction:str = "Consider yourself a function that takes the input of asked validation regex statement, and your output is '''Regex: {created regex}''' Do not give me an explanation, only give me a regex expression. Do not add any additional characters."
        prompt:str = f"{instruction}\nAsked regex statement: {description}."
        print("\nP: " + prompt)
        response = client.generate(model="codellama", prompt=prompt)
        answer = response['response']

        ollama_server_process.terminate()       #TODO: Manage the connecion. Do not terminate on every call.

        gencode:str = str(answer).strip().replace("Regex: ","").replace("```","").replace("`","")      #TODO: Output parsers here please!
        print("A: " + gencode)
        return gencode

if __name__ == "__main__":
    answer = OllamaModels(modelName='CodeLLaMa-v2').Generate("generate me an email regex, do not give me an explanation")
    print(answer)