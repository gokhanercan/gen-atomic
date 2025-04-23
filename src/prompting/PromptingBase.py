from abc import ABC, abstractmethod
from typing import Union
from prompting.Prompt import Prompt
from utility import StringHelper


class PromptingBase(ABC):
    """
    Base class for all prompting classes.
    #TODO: Add PromptDecorators like EmotionPrompt or ZeroCOT. WE should not need classes for those simple implementations.
    """

    def __init__(self, prompt: Union[str, Prompt]) -> None:
        super().__init__()
        if isinstance(prompt, str):
            if StringHelper.IsNullOrWhiteSpace(prompt):
                raise ValueError("Prompt cannot be empty or whitespace.")
            self.prompt: Prompt = Prompt(prompt)
        elif isinstance(prompt, Prompt):
            self.prompt: Prompt = prompt
        else:
            raise TypeError("Invalid type for prompt")

    # region Names and Identities
    def name(self) -> str:
        return str(type(self).__name__)

    def plain_name(self) -> str:
        return self.name().replace("Prompting", "").lower()

    def key(self):
        return f"{self.plain_name()}_{self.prompt.key()}"

    def __repr__(self) -> str:
        return self.key()

    def __str__(self) -> str:
        return self.key()

    # endregion

    @abstractmethod
    def generate(self):
        pass


class PromptingInfo(object):        # TODO: Support early prompting discovery.

    def __init__(self, plain_name: str) -> None:
        self.plain_name: str = plain_name


if __name__ == '__main__':
    PromptingBase("Hello")
