from prompting.Prompt import Prompt
from prompting.decorators.prompt_decorator_base import PromptDecoratorBase


class ZeroShotCoTDecorator(PromptDecoratorBase):
    """
    Decorator for zero-shot chain of thought prompting.
    This decorator modifies the prompt to encourage the model to think step-by-step without giving any examples.
    """

    def decorate(self, p: Prompt):
        p.text = f"Think step-by-step: {p.text}"

    def decorate_key(self, key: str):
        return f"{key}+CoT0"    # TODO: Should I add Cot prompt to the key?

