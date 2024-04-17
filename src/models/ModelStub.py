from models.ModelBase import ModelBase
from utility.StringHelper import Coelesce


class ModelStub(ModelBase):
    def __init__(self, stubUnit:str = None) -> None:
        super().__init__()
        self.StubUnit = stubUnit
        self.StubName = "Stub"

    def Generate(self, description: str) -> str:
        return Coelesce(self.StubUnit,f"Stub code for description '{description}'")  # type: ignore

    def ModelName(self):
        return self.StubName
