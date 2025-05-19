from unittest import TestCase

from models.ModelBase import ModelBase
from models.ModelFactory import ModelFactory
from models.StubModel import StubModel
from prompting.Prompt import Prompt
from prompting.PromptingBase import PromptingBase
from prompting.impl.DirectPrompting import DirectPrompting


class StaticModelConfiguration:

    def __init__(self, static_model_key:str, static_prompting_key:str):
        super().__init__()
        self.static_model_key = static_model_key
        self.static_prompting_key = static_prompting_key

    def key(self):
        return f"M({self.static_model_key })P({self.static_prompting_key})"

class StaticModelConfigurationTests(TestCase):
    def test_TwoStaticKeys_Concat(self):
        self.assertEqual(StaticModelConfiguration("np.stub", "direct").key(), "M(np.stub)P(direct)")


class ModelConfiguration(object):
    """
    Represents a dynamic model configuration with a specific hyperparameter set.
    """

    prompting: PromptingBase
    model: ModelBase

    def __init__(self, model: ModelBase, prompting: PromptingBase):
        super().__init__()
        self.model = model
        self.prompting = prompting

    def static_key(self):
        return f"M({self.model.Key()})P({self.prompting.static_key()})"     #TODO: Impl static key for models

    def key(self):
        return f"M({self.model.Key()})P({self.prompting.key()})"


class ModelConfigurationTests(TestCase):
    def test_Key_TextValue_HashTextAsKey(self):
        self.assertEqual(ModelConfiguration(StubModel("test"), DirectPrompting(Prompt("Hello prompt!"))).key(), "M(np.stub)P(direct_t:0b290fd)")


if __name__ == '__main__':
    # Explicit prompting with a text prompt
    print(ModelConfiguration(StubModel("test"), DirectPrompting("Hello prompt!")).key())
    print(ModelConfiguration(StubModel("test"), DirectPrompting(Prompt("Hello","P1001"))).key())

    # Explicit prompting with a Prompt reference
    # print(ModelConfiguration(ModelFactory().CreateModelByKey("ol.llama3"), DirectPrompting("Hello prompt!")).key())

    # Implicit prompting with a stub model
    # print(ModelConfiguration(StubModel("test"), DirectPrompting("Another prompt!")).Key())  # Explicit prompting
    #print(ModelConfiguration(StubModel("test")).Key())                                     # Implicit prompting TODO: Delete
