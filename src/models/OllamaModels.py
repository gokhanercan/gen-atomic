from models.ModelBase import ModelBase


class OllamaModels(ModelBase):
    def __init__(self, modelName:str) -> None:
        super().__init__()
        self.ModelName = modelName

    def Generate(self, description: str) -> str:
        raise Exception("TODO: not implemented. https://github.com/users/gokhanercan/projects/3/views/1?pane=issue&itemId=58245008")
