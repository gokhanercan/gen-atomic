from models.ModelBase import *
from utility import StringHelper
from utility.StringHelper import Coelesce


class StubModel(ModelBase, BaselineModel):
    def __init__(self, stubUnit:str = None) -> None:
        super().__init__()
        self.StubUnit = stubUnit
        self.StubName = None

    def Generate(self, description: str, langUnitInfo:LangUnitInfo) -> str:
        return Coelesce(self.StubUnit, f"Stub code for description '{description}'")  # type: ignore

    def ModelName(self):
        return StringHelper.Coelesce(self.StubName, super().Name())
