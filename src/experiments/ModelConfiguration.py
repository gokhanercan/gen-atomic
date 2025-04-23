from models.ModelBase import ModelBase
from models.ModelFactory import ModelFactory
from models.StubModel import StubModel
from prompting.Prompt import Prompt
from prompting.PromptingBase import PromptingBase
from prompting.direct.DirectPrompting import DirectPrompting


class ModelConfiguration(object):

    prompting: PromptingBase
    model: ModelBase

    def __init__(self, model: ModelBase, prompting: PromptingBase):
        super().__init__()
        self.model = model
        self.prompting = prompting

    def key(self):
        return f"M({self.model.Key()})P({self.prompting.key()})"


if __name__ == '__main__':
    # Explicit prompting with a text prompt
    print(ModelConfiguration(StubModel("test"), DirectPrompting("Hello prompt!")).key())
    print(ModelConfiguration(StubModel("test"), DirectPrompting(Prompt("Hello","P1001"))).key())

    # Explicit prompting with a Prompt reference
    # print(ModelConfiguration(ModelFactory().CreateModelByKey("ol.llama3"), DirectPrompting("Hello prompt!")).key())

    # Implicit prompting with a stub model
    # print(ModelConfiguration(StubModel("test"), DirectPrompting("Another prompt!")).Key())  # Explicit prompting
    #print(ModelConfiguration(StubModel("test")).Key())                                     # Implicit prompting TODO: Delete
