from abc import ABC, abstractmethod, ABCMeta

# from __future__ import annotations
from typing import Union, Type, Optional, Generic, TypeVar
from unittest import TestCase
from unittest.mock import Mock

from annotated_types import T
from pydantic import BaseModel, ConfigDict

from langunits.LangUnit import LangUnitInfo
from models.ModelBase import GenResponse, GenRequest
from prompting.Prompt import Prompt
from prompting.decorators.prompt_decorator_base import PromptDecoratorBase


class PromptingBase(ABC, Generic[T]):
    """
    Base class for all prompting classes.
    #TODO: Add PromptDecorators like EmotionPrompt or ZeroCOT. WE should not need classes for those simple implementations.
    """

    # region Names and Identities
    def name(self) -> str:
        return str(type(self).__name__)

    def plain_name(self) -> str:
        return self.name().replace("Prompting", "").lower()

    def static_key(self) -> str:
        return f"{self.plain_name()}"

    def key(self):
        return f"{self.plain_name()}"

    def __repr__(self) -> str:
        return self.key()

    def __str__(self) -> str:
        return self.key()

    # endregion

    @abstractmethod
    def create_default_instance(self, lang_unit_info: LangUnitInfo) -> T:
        """
        Creates a default prompt for this prompting class.
        :return: str
        """
        pass

    @abstractmethod
    def _generate(self, req: GenRequest) -> GenResponse:
        pass

    @staticmethod
    def apply_decorators(
        p: Prompt, prompt_decorators: list[PromptDecoratorBase]
    ) -> Prompt:
        """
        Applies a decorator to the prompt and return the decorated prompt.
        :param p:
        :param prompt_decorators:
        :param decorator: The decorator to apply.
        :return: The decorated prompt.
        """
        if prompt_decorators is None or len(prompt_decorators) == 0:
            return p
        import copy

        pNew: Prompt = copy.deepcopy(p)
        for decorator in prompt_decorators:
            decorator.decorate(pNew)
        return pNew


class PromptingBaseTests(TestCase):

    def test_apply_decorators__no_decorators_donothing(self):
        p = Prompt("Hello prompt!")
        decorators: list[PromptDecoratorBase] = []
        pNew = PromptingBase.apply_decorators(p, decorators)
        self.assertEqual(
            p, pNew, "Applying no decorators should return the same prompt."
        )

    def test_apply_decorators__multiple_decorators__apply(self):
        p = Prompt("Hello prompt!")

        def fake1_func(p: Prompt):
            p.text = p.text + " - Postfix"

        fake1 = Mock(spec=PromptDecoratorBase)
        fake1.decorate.side_effect = fake1_func

        def fake2_func(p: Prompt):
            p.text = "Prefix - " + p.text

        fake2 = Mock(spec=PromptDecoratorBase)
        fake2.decorate.side_effect = fake2_func

        pNew = PromptingBase.apply_decorators(p, [fake1, fake2])

        self.assertEqual("Prefix - Hello prompt! - Postfix", pNew.text)


class PromptingInfo(BaseModel):
    key: str
    plain_name: str
    type: ABCMeta
    doc: str = None

    model_config = ConfigDict(
        arbitrary_types_allowed=True
    )  # This is needed to allow non-pydantic types, ABCMeta in this case.

    def __eq__(self, other):
        if isinstance(other, PromptingInfo):
            return self.key == other.key
        return False


if __name__ == "__main__":
    pass
