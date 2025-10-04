from models.ModelBase import *
from utility import StringHelper
from utility.StringHelper import Coelesce


class StubModel(ModelBase, BaselineModel):
    def __init__(self, stub_unit: str = None) -> None:
        super().__init__()
        self.stub_unit = stub_unit
        self.stub_name = None

    def _generate_impl(self, req: GenRequest) -> GenResponse:
        generated: str = Coelesce(self.stub_unit, f"Stub code for description '{req.description}'")  # type: ignore
        return GenResponse(req.lang_unit_info, generated)

    def model_name(self):
        return StringHelper.Coelesce(self.stub_name, super().name())

    @staticmethod
    def fake_email(stubs: list["StubModel"]):
        fixed_regex: str = (
            r"""^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$"""
        )
        for stub in stubs:
            stub.stub_unit = fixed_regex  # type: ignore
            stub.stub_name = "EmailStub"
