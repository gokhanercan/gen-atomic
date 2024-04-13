from models.ModelBase import ModelBase


class ModelStub(ModelBase):
    def __init__(self, stubUnit:str = None) -> None:
        super().__init__()
        self.StubUnit = stubUnit

    def Generate(self, description: str) -> str:
        return self.StubUnit  # type: ignore