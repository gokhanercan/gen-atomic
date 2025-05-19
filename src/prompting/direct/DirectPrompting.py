from typing import Union

from prompting.Prompt import Prompt
from prompting.PromptingBase import PromptingBase
from utility import StringHelper


class DirectPrompting(PromptingBase):
    """
    DirectPrompting is a simple/vanilla prompting class that uses a single prompt string.
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

    def generate(self):
        pass


if __name__ == '__main__':
    # DirectPrompting("Hello")
    DirectPrompting(Prompt("Hello prompt!"))
