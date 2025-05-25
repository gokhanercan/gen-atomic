from prompting.Prompt import Prompt
from prompting.decorators.prompt_decorator_base import PromptDecoratorBase


class EmotionDecorator(PromptDecoratorBase):
    """
    Decorator for emotion prompting.
    """

    def decorate(self, p: Prompt):
        p.text = f"Think step-by-step: {p.text}"

    def decorate_key(self, key: str):
        return f"{key}+Emo"

