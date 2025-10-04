from abc import abstractmethod, ABCMeta
from typing import Type

from pydantic import BaseModel, ConfigDict
from prompting.Prompt import Prompt
from prompting.repo.prompt_repository_base import PromptRepositoryBase


class PromptDecoratorBase:
    """
    Base class for prompt decorators.
    This class should be inherited by any decorator that modifies the behavior of prompts.
    """

    # region Names and Identities
    def name(self) -> str:
        return str(type(self).__name__)

    def plain_name(self) -> str:
        return self.name().replace("Decorator", "").lower()

    def static_key(self) -> str:
        return f"{self.plain_name()}"

    def key(self) -> str:
        return f"{self.static_key()}"

    def __repr__(self) -> str:
        return self.static_key()

    def __str__(self) -> str:
        return self.static_key()

    # endregion

    @abstractmethod
    def decorate(self, prompt: Prompt):
        """
        Applies the decorator to the prompt reference.
        :param prompt:
        :return:
        """
        pass

    @abstractmethod
    def decorate_key(self, key: str):
        """Decorates the key for the prompt. Decorators should modify the key to reflect their changes."""
        pass

    def create_default_instance(
        self, repo: PromptRepositoryBase, lang_unit_name: str | None = None
    ) -> "PromptDecoratorBase":
        """
        Factory: Creates a default instance of the decorator using the repository. Override this method in subclasses if needed.
        :param repo:
        :param lang_unit_name:
        :return:
        """
        return self.__class__()


class PromptDecoratorInfo(BaseModel):
    key: str
    plain_name: str
    type: Type[PromptDecoratorBase]
    doc: str = None

    model_config = ConfigDict(arbitrary_types_allowed=True)
