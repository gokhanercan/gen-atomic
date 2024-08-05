from abc import ABC, abstractmethod

from langunits.LangUnit import LangUnitInfo
from prompting import Prompt


class PromptingBase(ABC):

    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def Generate(self)->Prompt:
        pass

    def GenText(self, langUnitInfo:LangUnitInfo, desc:str)->str:
        pass
