from models.ModelBase import ModelBase
from models.StubModel import StubModel
from prompting.PromptingBase import PromptingBase
from prompting.direct.DirectPrompting import DirectPrompting


class ModelConfiguration(object):

    def __init__(self, model: ModelBase, prompting: PromptingBase):
        super().__init__()
        self.Model = model
        self.Prompting = prompting

    def Key(self):
        return f"M({self.Model.Key()})P({self.Prompting.Key()})"


if __name__ == '__main__':
    print(ModelConfiguration(StubModel("test"), DirectPrompting("Hello prompt!")).Key())    #Explicit prompting
    print(ModelConfiguration(StubModel("test"), DirectPrompting("Another prompt!")).Key())  #Explicit prompting
    #print(ModelConfiguration(StubModel("test")).Key())                                     #Implicit prompting TODO: Delete
