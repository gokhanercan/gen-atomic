from abc import ABC, abstractmethod
from typing import Union, Type, Optional
from pydantic import BaseModel


class PromptingBase(ABC):
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
    def generate(self):
        pass


class PromptingInfo(BaseModel):
    key: str
    plain_name: str
    type: Optional[Type] = None
    doc: str = None


if __name__ == '__main__':
    # print(PromptingInfo(plain_name="test"))
    pass