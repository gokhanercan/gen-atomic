from prompting.Prompt import Prompt
from prompting.decorators.prompt_decorator_base import PromptDecoratorBase
from prompting.repo.prompt_repository_base import PromptRepositoryBase


class HiddenZeroShotCoTDecorator(PromptDecoratorBase):
    """
    Decorator for zero-shot chain of thought prompting.
    This decorator modifies the prompt to encourage the model to think step-by-step without giving any examples.
    It is 'Hidden' because it does not ask for the explanation to be outputted, but rather to think through the reasoning process internally.
    """

    def __init__(self, zero_shot: Prompt):
        super().__init__()
        self.zero_shot: Prompt = zero_shot

    def decorate(self, p: Prompt):
        p.text = f"{self.zero_shot.text}.{p.text}"

    def decorate_key(self, key: str):
        my_key: str = f"HCOT0_{self.zero_shot.key()}"
        return f"{key}+{my_key}"

    def create_default_instance(self, repo: PromptRepositoryBase, lang_unit_name: str | None = None) -> "PromptDecoratorBase":
        p: Prompt = repo.get_by_type_key(self.static_key())
        return self.__class__(p)
