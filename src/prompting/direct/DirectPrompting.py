from prompting.Prompt import Prompt
from prompting.PromptingBase import PromptingBase


class DirectPrompting(PromptingBase):
    """
    DirectPrompting is a simple/vanilla prompting class that uses a single prompt string.
    """


    def generate(self):
        pass


if __name__ == '__main__':

    DirectPrompting("Hello")
    DirectPrompting(Prompt("Hello prompt!"))
