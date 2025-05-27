from prompting.Prompt import Prompt
from prompting.decorators.prompt_decorator_base import PromptDecoratorBase


class EmotionDecorator(PromptDecoratorBase):
    """
    Decorator imlementation for emotion prompting.
    """

    _EMOTION_PROMPT_AS_PREFIX:Prompt = Prompt("I'm having a really hard time getting this right and I feel a bit stuck")
    # TODO: Add more emotions and their prompts as needed to the prompt repository.

    def decorate(self, p: Prompt):
        p.text = f"{self._EMOTION_PROMPT_AS_PREFIX.text}.{p.text}"

    def decorate_key(self, key: str):
        my_key:str = f"Emo_{self._EMOTION_PROMPT_AS_PREFIX.key()}"
        return f"{key}+{my_key}"
