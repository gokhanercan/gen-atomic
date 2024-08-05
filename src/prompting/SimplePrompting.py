from langunits.LangUnit import LangUnit, LangUnitInfo
from prompting import Prompt
from prompting.PromptingBase import PromptingBase


class SimplePrompting(PromptingBase):

    def __init__(self, prompt:Prompt) -> None:
        super().__init__()
        self.Prompt:Prompt = prompt

    def Generate(self) -> Prompt:
        return self.Prompt      #TODO:

    def GenText(self, langUnitInfo:LangUnitInfo, desc:str)->str:
        return self.Prompt.Render(langUnitInfo.PromptText,desc)

