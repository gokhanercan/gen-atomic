from src.models.ModelBase import ModelBase

class OllamaModels(ModelBase):
    def __init__(self, modelName:str) -> None:
        super().__init__()
        self.ModelName = modelName

    def Generate(self, description: str) -> str:
        raise Exception("not implemented.") #pass modelName and run llama2