from abc import abstractmethod, ABC

from langunits.LangUnit import LangUnit
from prompting.Prompt import Prompt


class PromptRepositoryBase(ABC):

    @abstractmethod
    def get_prompt(self, pid: str) -> Prompt:
        pass

    def get_default_prompt(self, lang_unit_name: str | None = None) -> Prompt:
        if lang_unit_name:
            return self.get_prompt(f"{lang_unit_name.lower()}_default")
        else:
            return self.get_prompt("default")

    def get_by_type_key(self, type_key: str) -> Prompt:
        """
        Returns the default prompt for a given type (Prompting or PromptDecorator) key.
        :param type_key: The key of the type for which to get the default prompt.
        :return: The default prompt for the specified type key.
        """
        return self.get_prompt(f"{type_key.lower()}")

    @abstractmethod
    def add_prompt(self, prompt: Prompt):
        pass
