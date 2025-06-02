from models.ModelBase import *
from utility import StringHelper
from utility.StringHelper import Coelesce


class StubModel(ModelBase, BaselineModel):
    def __init__(self, stubUnit: str = None) -> None:
        super().__init__()
        self.StubUnit = stubUnit
        self.StubName = None

    def _generate_impl(self, req: GenRequest) -> GenResponse:
        generated: str = Coelesce(self.StubUnit, f"Stub code for description '{req.description}'")  # type: ignore
        return GenResponse(req.lang_unit_info, generated)

    def ModelName(self):
        return StringHelper.Coelesce(self.StubName, super().Name())

    @staticmethod
    def fake_email(stubs: list["StubModel"]):
        fixed_regex: str = r"""^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$"""
        for stub in stubs:
            stub.StubUnit = fixed_regex  # type: ignore
            stub.StubName = "EmailStub"
