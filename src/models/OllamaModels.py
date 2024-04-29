from models.ModelBase import ModelBase


class OllamaModels(ModelBase):
    def __init__(self, modelName:str) -> None:
        super().__init__()
        self.ModelName = modelName

    def Generate(self, description: str) -> str:

        #1. CONFIG: IP Address, Port. ModelName, ConfName, Path....
        #2. INSTALLATION: WSL, Pytorch, LangChain, pip, C++Comp,
        #3. PROMPTS:

        P1:str = "give me the result in Regex format only. Do not include natural language text."

        raise Exception("TODO: not implemented. https://github.com/users/gokhanercan/projects/3/views/1?pane=issue&itemId=58245008")
