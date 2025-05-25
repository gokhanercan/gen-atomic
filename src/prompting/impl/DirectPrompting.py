from __future__ import annotations

from typing import Union, __all__

from langunits.LangUnit import LangUnitInfo
from prompting.Prompt import Prompt
from prompting.PromptingBase import PromptingBase
from prompting.decorators.prompt_decorator_base import PromptDecoratorBase
from utility import StringHelper


class DirectPrompting(PromptingBase):
    """
    DirectPrompting is a simple/vanilla prompting class that uses a single prompt string.
    """

    def __init__(self, prompt: Prompt, prompt_decorators:list[PromptDecoratorBase] | None = None) -> None:
        super().__init__()
        if isinstance(prompt, str):
            if StringHelper.IsNullOrWhiteSpace(prompt):
                raise ValueError("Prompt cannot be empty or whitespace.")
            self.prompt: Prompt = Prompt(prompt)
        elif isinstance(prompt, Prompt):
            self.prompt: Prompt = prompt
        else:
            raise TypeError("Invalid type for prompt")
        self.prompt_decorators:list[PromptDecoratorBase] = prompt_decorators

    def key(self):
        if hasattr(self,"prompt"):      #dynamic key
            return f"{self.plain_name()}_{self.prompt.key()}"
        else:
            return super().static_key()

    def generate(self):
        pass

    # region Defaults

    def _create_default_prompt(self,lang_unit_info:LangUnitInfo) -> Prompt:
        """
        Creates a default prompt for this prompting class.
        :return: Prompt
        """
        lang_desc: str = lang_unit_info.PromptText
        instruction: str = (f"Consider yourself a function that takes the input of asked {lang_desc} statement, and "
                            f"your output should be a markdown code snippet formatted in the following schema, including "
                            f"the leading and trailing \"```{lang_desc}\" and \"```\". Do not give me an explanation, only give "
                            f"me a {lang_desc} expression. Do not add any additional characters. Asked {lang_desc} statement: [CODE_DESCRIPTION]].")
        return Prompt(instruction)

    def create_default_instance(self,lang_unit_info:LangUnitInfo) -> 'DirectPrompting':
        return self.__class__(self._create_default_prompt(lang_unit_info))

    # endregion


if __name__ == '__main__':
    # DirectPrompting("Hello")
    DirectPrompting(Prompt("Hello prompt!"))