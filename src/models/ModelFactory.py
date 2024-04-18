from models.ModelBase import ModelBase
from models.RandomModel import RandomModel
from models.StubModel import StubModel


class ModelFactory(object):

    def __init__(self) -> None:
        super().__init__()

    def ListModelNames(self):
        """
        Lists all available model names
        :return:
        """
        return ["Stub","Random"]

    def CreateAllModels(self):
        """
        Creates instances of all available models.
        :return:
        """
        models = []
        for modelName in self.ListModelNames():
            m:ModelBase = self.Create(modelName)
            models.append(m)
        return models

    def Create(self, modelName:str):
        if(modelName == "Stub"):
            return StubModel()
        elif(modelName == "Random"):
            return RandomModel()
        else:
            raise Exception("no provider!")