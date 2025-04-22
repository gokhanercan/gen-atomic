from abc import ABC, abstractmethod

from langunits.LangUnit import LangUnitInfo
from utility import StringHelper
from utility.StringHelper import StringHelperTest


class PromptingBase(ABC):
    """
    Base class for all prompting classes.
    #TODO: Add PromptDecorators like EmotionPrompt or ZeroCOT. WE should not need classes for those simple implementations.
    """

    def __init__(self, prompt:str) -> None:      #langUnit:LangUnitInfo
        super().__init__()
        if StringHelper.IsNullOrWhiteSpace(prompt): raise ValueError("Prompt cannot be empty or whitespace.")
        self.Prompt: str = prompt       #TODO: Add id and defaultPrompt support. Provide PromptFactory.

    #region Names and Identities
    def Name(self)->str:
        return str(type(self).__name__)
    def PlainName(self)->str:
        return self.Name().replace("Prompting","")
    def Key(self):          #Implementations should override this.
        return f"{self.PlainName()}_t:{self.GetPromptHash()}"
    def __repr__(self) -> str:
        return f"M[{self.Key()}]"
    def __str__(self) -> str:
        return f"M[{self.Key()}]"

    @abstractmethod
    def Generate(self):
        pass

    def GetPromptHash(self)->str:
        import hashlib
        sha1 = hashlib.sha1(self.Prompt.encode('utf-8')).hexdigest()
        return sha1[:7]


class PromptingInfo(object):

    def __init__(self, plainName:str) -> None:
        self.PlainName = plainName