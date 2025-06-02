from __future__ import annotations
from deprecated import deprecated

from langunits.LangUnit import LangUnitInfo
from models.ModelBase import GenResponse, GenRequest
from prompting.Prompt import Prompt
from prompting.PromptingBase import PromptingBase
from prompting.decorators.prompt_decorator_base import PromptDecoratorBase
from utility import StringHelper


class DirectPrompting(PromptingBase):
    """
    DirectPrompting is a simple/vanilla prompting that uses a single prompt in a single request.
    """

    def __init__(self, prompt: Prompt, prompt_decorators: list[PromptDecoratorBase] | None = None) -> None:
        super().__init__()
        if isinstance(prompt, str):
            if StringHelper.IsNullOrWhiteSpace(prompt):
                raise ValueError("Prompt cannot be empty or whitespace.")
            self.prompt: Prompt = Prompt(prompt)
        elif isinstance(prompt, Prompt):
            self.prompt: Prompt = prompt
        else:
            raise TypeError("Invalid type for prompt")
        if prompt_decorators is None:
            prompt_decorators = []
        self.prompt_decorators: list[PromptDecoratorBase] = prompt_decorators

    def key(self) -> str:
        key: str = ""
        if hasattr(self, "prompt"):  # dynamic key
            key = f"{self.plain_name()}_{self.prompt.key()}"
        else:
            key = super().static_key()

        # Apply decorators
        if self.prompt_decorators:
            for d in sorted(self.prompt_decorators, key=lambda x: x.key()):
                key = d.decorate_key(key)
        return key

    def _generate(self, req: GenRequest) -> GenResponse:
        eff_prompt: Prompt = PromptingBase.apply_decorators(self.prompt, self.prompt_decorators)
        lang_unit_desc: str = req.lang_unit_info.PromptText
        final_prompt: str = eff_prompt.text.replace("[DESC]", req.description).replace("[LANG_UNIT_DESC]", lang_unit_desc)

        # promptColored: str = f"{instruction}\nAsked {lang_desc} statement: {Fore.BLUE}{description}{Fore.RESET}."
        # print(f"\nP:{promptColored}")
        # print(Fore.RESET)

        # model call
        req2: GenRequest = req.clone_to_final_prompt(final_prompt)
        res: GenResponse = req.gen_model.generate(req2)
        return res

    # region Defaults
    def _create_default_prompt(self, lang_unit_info: LangUnitInfo) -> Prompt:
        """
        Creates a default prompt for this prompting class.
        :return: Prompt
        """
        # TODO: Load from the prompt repository
        lang_desc: str = lang_unit_info.PromptText
        instruction: str = (
            f"Consider yourself a function that takes the input of asked {lang_desc} statement, and "
            f"your output should be a markdown code snippet formatted in the following schema, including "
            f'the leading and trailing "```{lang_desc}" and "```". Do not give me an explanation, only give '
            f"me a {lang_desc} expression. Do not add any additional characters. Asked {lang_desc} statement: [CODE_DESCRIPTION]]."
        )
        return Prompt(instruction)

    def create_default_instance(self, lang_unit_info: LangUnitInfo) -> "DirectPrompting":
        return self.__class__(self._create_default_prompt(lang_unit_info))

    # endregion


if __name__ == "__main__":
    DirectPrompting(Prompt("Hello prompt!"))
