import copy
from abc import ABC, abstractmethod, ABCMeta
from dataclasses import field

from langunits.LangUnit import LangUnitInfo
from utility import StringHelper
from data.dataset import *


class BaselineModel(ABC):
    """
    This is a marker-type to indicate fake/stub/ummy baseline models.
    """

    pass


class ModelInfo(object):
    def __init__(
        self,
        plainName: str,
        providerName: Optional[str] = None,
        providerAbbreviation: Optional[str] = None,
    ) -> None:
        super().__init__()
        self.PlainName: str = plainName
        self.ProviderName: Optional[str] = providerName
        self.ProviderAbbreviation: Optional[str] = providerAbbreviation

    def Key(self) -> str:
        abbr: str = StringHelper.Coelesce(self.ProviderAbbreviation, "np")
        return f"{abbr.lower()}.{self.PlainName.lower()}"

    def __str__(self) -> str:
        return self.Key()

    def __repr__(self) -> str:
        return self.Key()

    def __eq__(self, other):
        if isinstance(other, ModelBase):
            return self.Key() == other.Key()
        return False


@dataclass
class ModelProviderMeta:
    Name: str
    Type: ABCMeta
    Abbreviation: str

    def __eq__(self, other):
        if isinstance(other, ModelBase):
            return self.Name == other.Name
        return False


@dataclass
class StandaloneModelMeta:
    Name: str
    Type: ABCMeta
    IsBaseline: bool = field(default=False)


@dataclass
class ModelMeta:
    """
    Represents effective metadata information for all available models.
    """

    Name: str
    PlainName: str
    Key: str
    StandaloneModelMeta: StandaloneModelMeta = None
    ModelProviderMeta: ModelProviderMeta = None

    # TODO: Add configs.
    @property
    def IsStandalone(self) -> bool:
        return self.StandaloneModelMeta is not None

    @property
    def IsBaseline(self) -> bool:
        if self.IsStandalone:
            return self.StandaloneModelMeta.IsBaseline
        else:
            return False  # We can't define baseline model by providers


class ModelBase(ABC):
    def __init__(self, modelMeta: ModelMeta | None = None) -> None:
        super().__init__()
        self.ModelMeta: ModelMeta | None = modelMeta  # TODO: Index sets it!

    # region Names and Identities
    def Name(self) -> str:
        return str(type(self).__name__)

    def PlainName(self) -> str:
        return self.Name().replace("Model", "").replace("Provider", "")

    def ProviderName(self) -> str:
        return "NoProvider"

    def ProviderAbbreviation(self) -> str:
        return "np"

    def Key(self):
        return self.GetModelConf().Key()

    def __repr__(self) -> str:
        return f"M[{self.Key()}]"

    def __str__(self) -> str:
        return f"M[{self.Key()}]"

    def GetModelConf(self) -> ModelInfo:
        return ModelInfo(self.PlainName(), self.ProviderName(), self.ProviderAbbreviation())

    # endregion

    def generate(self, req: "GenRequest") -> "GenResponse":
        res: GenResponse = self._generate_impl(req)
        return res

    @abstractmethod
    def _generate_impl(self, req: "GenRequest") -> "GenResponse":
        pass


@dataclass
class GenRequest:
    lang_unit_info: LangUnitInfo
    description: str
    gen_model: ModelBase  # The model which is responsible for generation. Managers and Evaluators will be different.
    final_prompt: str | None

    def clone(self):
        """
        Creates the deep copy of this request.
        :return:
        """
        c = copy.deepcopy(self)
        return c

    def clone_to_final_prompt(self, final_prompt: str) -> "GenRequest":
        c = self.clone()
        c.final_prompt = final_prompt
        return c


@dataclass
class GenResponse:
    lang_unit_info: LangUnitInfo
    raw_generated: str
