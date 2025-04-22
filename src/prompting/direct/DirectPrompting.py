from prompting.PromptingBase import PromptingBase


class DirectPrompting(PromptingBase):
    """
    DirectPrompting is a simple/vanilla prompting class that uses a single prompt string.
    """

    def __init__(self, prompt: str) -> None:
        super().__init__(prompt)

    def Generate(self):
        pass

if __name__ == '__main__':
    DirectPrompting("Hello")