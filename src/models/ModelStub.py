from models.ModelBase import ModelBase
from utility.StringHelper import Coelesce


class ModelStub(ModelBase):
    def __init__(self, stubUnit:str = None) -> None:
        super().__init__()
        self.StubUnit = stubUnit

    def Generate(self, description: str) -> str:
        return Coelesce(self.StubUnit,"stub code")  # type: ignore