from prompting.Prompt import Prompt
from prompting.decorators.prompt_decorator_base import PromptDecoratorBase
from prompting.repo.prompt_repository_base import PromptRepositoryBase


class EmotionDecorator(PromptDecoratorBase):
    """
    Decorator implementation for emotion prompting.
    """

    def __init__(self, emotion: Prompt) -> None:
        super().__init__()
        self.Emotion: Prompt = emotion

    def decorate(self, p: Prompt):
        p.text = f"{self.Emotion.text}.{p.text}"

    def decorate_key(self, key: str):
        my_key: str = f"Emo_{self.Emotion.key()}"
        return f"{key}+{my_key}"

    def create_default_instance(
        self, repo: PromptRepositoryBase, lang_unit_name: str | None = None
    ) -> "PromptDecoratorBase":
        p: Prompt = repo.get_by_type_key(self.static_key())
        return self.__class__(p)
