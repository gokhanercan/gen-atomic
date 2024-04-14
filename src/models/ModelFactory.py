from models.ModelStub import ModelStub


class ModelFactory(object):

    def __init__(self) -> None:
        super().__init__()

    def ListModelNames(self):
        return ["Stub","Random"]

    @staticmethod
    def Create(modelName:str):
        if(modelName == "Stub"):
            return ModelStub()
        elif(modelName == "Random"):
            return ModelStub()      #Random model here.
        else:
            raise Exception("no provider!")