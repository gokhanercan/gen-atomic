from abc import ABC, abstractmethod, ABCMeta
# from __future__ import annotations
from typing import Union, Type, Optional, Generic, TypeVar
from annotated_types import T
from pydantic import BaseModel, ConfigDict

from langunits.LangUnit import LangUnitInfo


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
    def create_default_instance(self, lang_unit_info:LangUnitInfo) -> T:
        """
        Creates a default prompt for this prompting class.
        :return: str
        """
        pass

    @abstractmethod
    def generate(self):
        pass


class PromptingInfo(BaseModel):
    key: str
    plain_name: str
    type: ABCMeta
    doc: str = None

    model_config = ConfigDict(arbitrary_types_allowed=True) # This is needed to allow non-pydantic types, ABCMeta in this case.


if __name__ == '__main__':
    # print(PromptingInfo(plain_name="test"))
    pass