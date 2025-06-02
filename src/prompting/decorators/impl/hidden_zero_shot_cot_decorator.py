from prompting.Prompt import Prompt
from prompting.decorators.prompt_decorator_base import PromptDecoratorBase


class HiddenZeroShotCoTDecorator(PromptDecoratorBase):
    """
    Decorator for zero-shot chain of thought prompting.
    This decorator modifies the prompt to encourage the model to think step-by-step without giving any examples.
    # TODO: Hidden-CTO or update the oginial prompt text. Prompts are related?
    """

    _HIDDEN_COT_PROMPT_AS_PREFIX: Prompt = Prompt("Think step by step and show your reasoning before outputting the final [LANG_DESC] code inside triple backticks.")

    def decorate(self, p: Prompt):
        p.text = f"{self._HIDDEN_COT_PROMPT_AS_PREFIX.text}.{p.text}"

    def decorate_key(self, key: str):
        my_key: str = f"HCOT0_{self._HIDDEN_COT_PROMPT_AS_PREFIX.key()}"
        return f"{key}+{my_key}"
