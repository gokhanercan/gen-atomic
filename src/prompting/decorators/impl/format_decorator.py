from enum import auto, Enum

from models.ModelBase import GenResponse
from prompting.Prompt import Prompt
from prompting.decorators.format_parser import FormatParserBase
from prompting.decorators.prompt_decorator_base import PromptDecoratorBase
from prompting.repo.prompt_repository_base import PromptRepositoryBase


class FormatType(Enum):
    MARKDOWN = ("Markdown", "md")
    JSON = ("Json", "js")

    def __init__(self, value: str, abbreviation: str):
        self._value_ = value
        self.abbreviation = abbreviation

    @property
    def label(self) -> str:
        return self.name.capitalize()

    @property
    def key(self):
        return self.abbreviation


class FormatDecorator(PromptDecoratorBase, FormatParserBase):
    """
    Decorates the prompt with the expected output format.
    # TODO: Make it a parser a the same time! Parse what you ask.
    """

    def __init__(self, format: Prompt, format_type: FormatType = FormatType.MARKDOWN) -> None:
        super().__init__()
        self.format_type: FormatType = format_type
        self.format = format
        # self._PROMPT: Prompt = Prompt(  # TODO: Load the text from the prompt repository
        #     f"Wrap the Output with the following {self.format_type.label} code block: ```\nOutput\n```"
        # )

    def decorate(self, p: Prompt):
        p.text = f"{p.text} {self.format}"

    def decorate_key(self, key: str):
        my_key: str = f"Fmt_{self.format_type.key}_{self.format.key}"
        return f"{key}+{my_key}"

    def create_default_instance(self, repo: PromptRepositoryBase, lang_unit_name: str | None = None) -> "PromptDecoratorBase":
        p: Prompt = repo.get_by_type_key(self.static_key())
        return self.__class__(p)

    def parse(self, res: GenResponse) -> GenResponse:
        raise Exception("TODO: FormatDecorator does not support parsing yet. Use FormatParserBase instead.")


if __name__ == "__main__":

    f = FormatDecorator(
        Prompt("Wrap the Output with the following {self.format_type.label} code block: ```\nOutput\n```", "1"),
        FormatType.MARKDOWN,
    )
    print(f.format)
    print("\n" + f.format.text)
    print(f.format_type.key)
    print("Decorate Key:", f.decorate_key("TestKey"))
