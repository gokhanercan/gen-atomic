import streamlit as st

from models.ModelBase import ModelBase
from models.OllamaModels import OllamaModels
from models.RandomModel import RandomModel
from models.CodeLlamaModel import CodeLlamaModel
from models.StubModel import StubModel



class ModelFactory(object):

    def __init__(self) -> None:
        super().__init__()
        self.st = st

    def ListModelNames(self):
        """
        Lists all available model names
        :return:
        """
        return ["Stub","Random","CodeLlama"]

    def CreateAllModels(self):
        """
        Creates instances of all available models.
        :return:
        """
        models = []
        for modelName in self.ListModelNames():
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
        elif (modelName == "CodeLLaMa-v2"):
            return OllamaModels("CodeLLaMa-v2")     #TODO:
        else:
            raise Exception("no provider!")