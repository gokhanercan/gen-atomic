from models.ModelBase import ModelBase
from models.OllamaModels import OllamaModels
from models.RandomModel import RandomModel
from models.CodeLlamaModel import CodeLlamaModel
from models.StubModel import StubModel


class ModelFactory(object):

    def __init__(self) -> None:
        super().__init__()


    def ListModelNames(self):
        """
        Lists all available model names
        :return:
        """
        return ["CodeLlama","CodeLLaMa-v2"]

    def ListFakeModelNames(self):
        """
        Lists all available fake model names
        :return:
        """
        return ["Stub","Random"]

    def CreateFakeModels(self):
        models = []
        for modelName in self.ListFakeModelNames():
            m: ModelBase = self.Create(modelName)
            models.append(m)
        return models

    def CreateAllModels(self):
        """
        Creates instances of all available models.
        :return:
        """
        models = []
        for modelName in self.ListModelNames() + self.ListFakeModelNames():
            m: ModelBase = self.Create(modelName)
            models.append(m)
        return models

    def Create(self, modelName: str):
        if(modelName == "Stub"):
            return StubModel()
        elif(modelName == "Random"):
            return RandomModel()
        elif (modelName == "CodeLlama"):
            return CodeLlamaModel()
        elif (modelName == "CodeLLaMa-v2"):         #TODO:Merge ollama models.
            return OllamaModels("CodeLLaMa-v2")
        else:
            raise Exception(f"No model implementation found for '{modelName}'.")