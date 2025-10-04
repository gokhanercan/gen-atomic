import copy
from abc import ABC, abstractmethod, ABCMeta
from dataclasses import field
from langunits.LangUnit import LangUnitInfo
from utility import StringHelper
from data.Dataset import *


class BaselineModel(ABC):
    """
    This is a marker-type to indicate fake/stub/dummy baseline models.
    """

    pass


class ModelInfo(object):
    def __init__(
        self,
        plain_name: str,
        provider_name: Optional[str] = None,
        provider_abbreviation: Optional[str] = None,
    ) -> None:
        super().__init__()
        self.plain_name: str = plain_name
        self.provider_name: Optional[str] = provider_name
        self.provider_abbreviation: Optional[str] = provider_abbreviation

    def key(self) -> str:
        abbr: str = StringHelper.Coelesce(self.provider_abbreviation, "np")
        return f"{abbr.lower()}.{self.plain_name.lower()}"

    def __str__(self) -> str:
        return self.key()

    def __repr__(self) -> str:
        return self.key()

    def __eq__(self, other):
        if isinstance(other, ModelBase):
            return self.key() == other.key()
        return False


@dataclass
class ModelProviderMeta:
    name: str
    type: ABCMeta
    abbreviation: str

    def __eq__(self, other):
        if isinstance(other, ModelBase):
            return self.name == other.name
        return False


@dataclass
class StandaloneModelMeta:
    name: str
    type: ABCMeta
    is_baseline: bool = field(default=False)


@dataclass
class ModelMeta:
    """
    Represents effective metadata information for all available models.
    """

    name: str
    plain_name: str
    key: str
    standalone_model_meta: StandaloneModelMeta = None
    model_provider_meta: ModelProviderMeta = None

    # TODO: Add configs.
    @property
    def is_standalone(self) -> bool:
        return self.standalone_model_meta is not None

    @property
    def is_baseline(self) -> bool:
        if self.is_standalone:
            return self.standalone_model_meta.is_baseline
        else:
            return False  # We can't define baseline model by providers


@dataclass
class GenRequest:
    lang_unit_info: LangUnitInfo
    description: str
    gen_model: any  # The model which is responsible for generation. Managers and Evaluators will be different.
    final_prompt: str | None

    def clone(self) -> "GenRequest":
        """
        Creates the deep copy of this request.
        :return:
        """
        return copy.deepcopy(self)

    def clone_to_final_prompt(self, final_prompt: str) -> "GenRequest":
        c = self.clone()
        c.final_prompt = final_prompt
        return c


@dataclass
class GenResponse:
    lang_unit_info: LangUnitInfo
    raw_generated: str


class ModelBase(ABC):
    def __init__(self, model_meta: ModelMeta | None = None) -> None:
        super().__init__()
        self.model_meta: ModelMeta | None = model_meta  # TODO: Index sets it!

    # region Names and Identities
    def name(self) -> str:
        return str(type(self).__name__)

    def plain_name(self) -> str:
        return self.name().replace("Model", "").replace("Provider", "")

    # TODO: Convert to @property
    def provider_name(self) -> str:
        return "NoProvider"

    def provider_abbreviation(self) -> str:
        return "np"

    def key(self):
        return self.get_model_conf().key()

    def __repr__(self) -> str:
        return f"M[{self.key()}]"

    def __str__(self) -> str:
        return f"M[{self.key()}]"

    @deprecated("Use Key/key instead.")
    def get_model_conf(self) -> ModelInfo:
        return ModelInfo(self.plain_name(), self.provider_name(), self.provider_abbreviation())

    # endregion

    def generate(self, req: "GenRequest") -> "GenResponse":
        if not req.final_prompt:
            raise ValueError(
                "Final prompt must be calculated in the request before generating. Check your prompting implementation."
            )
        res: GenResponse = self._generate_impl(req)
        return res

    @abstractmethod
    def _generate_impl(self, req: "GenRequest") -> "GenResponse":
        pass
