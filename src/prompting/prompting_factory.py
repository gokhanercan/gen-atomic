from langunits.LangUnit import LangUnitInfo
from prompting.Prompt import Prompt
from prompting.PromptingBase import PromptingInfo, PromptingBase
from prompting.decorators.prompt_decorator_base import (
    PromptDecoratorInfo,
    PromptDecoratorBase,
)
from prompting.impl.DirectPrompting import DirectPrompting
from prompting.repo.inmemory_prompt_repository import InMemoryPromptRepository
from prompting.repo.prompt_repository_base import PromptRepositoryBase
from utility import Discovery


class PromptingFactory(object):

    def __init__(self, repository: PromptRepositoryBase) -> None:
        super().__init__()
        self.promptings_meta: dict[str, PromptingInfo] = self.discover_promptings()
        self.prompt_decorator_meta: dict[str, PromptDecoratorInfo] = self.discover_prompt_decorators()
        self.repository: PromptRepositoryBase = repository

    def discover_promptings(self) -> dict[str, PromptingInfo]:
        types = Discovery.find_subclasses("prompting", PromptingBase, "impl")
        metas: dict[str, PromptingInfo] = {}
        for t in types:
            name: str = t.__name__
            p: PromptingBase = t.__new__(t)
            key: str = p.static_key()  # TODO: static or dynamic key?
            meta = PromptingInfo(key=key, plain_name=p.plain_name(), type=t, doc=t.__doc__)
            metas[key] = meta
        return metas

    def get_all_prompting_meta(self) -> list[PromptingInfo]:
        return [v for k, v in self.promptings_meta.items()]

    def get_all_prompting_keys(self) -> list[str]:
        return [m.key for m in self.get_all_prompting_meta()]

    # _ALL_UNITS_PROMPT: str = (
    #     "You are a function that receives a [LANG_UNIT_DESC] instruction.\n"
    #     "Return **only** a single valid [LANG_UNIT_DESC] expression formatted according to the specified output format.\n"
    #     "Do not explain or comment.\n\n"
    #     "Instruction: [GEN_ATOMIC_UNIT_DESC]"
    # )
    # _CODE_FORMAT_PROMPT: str = (
    #     "Wrap the output with the following markdown code block:\n" "```\n" "```[LANG_UNIT_DESC]\n" "[CONTENT]\n" "```"
    # )

    def create_default(self, lang_unit_name: str | None = None) -> PromptingBase:
        default_prompt: Prompt = self.repository.get_default_prompt(lang_unit_name)
        return DirectPrompting(default_prompt)  # This is the default prompting implementation

    def create_prompting_instance(self, p_key: str, lang_unit_info: LangUnitInfo) -> PromptingBase:
        info: PromptingInfo = self.promptings_meta.get(p_key, None)
        if info is None:
            raise ValueError(f"Prompting with key '{p_key}' not found.")

        t = info.type  # TODO: This Type is MetaABC in ModelFactory, but throws error here. Why?
        p: PromptingBase = t.__new__(t)
        if t != type(p):
            raise TypeError(f"Type mismatch: Expected {t}, got {type(p)}")
        p = p.create_default_instance(self.repository, lang_unit_info.Name if lang_unit_info else None)
        return p

    # region Decorators
    def discover_prompt_decorators(self) -> dict[str, PromptDecoratorInfo]:
        types = Discovery.find_subclasses("prompting.decorators", PromptDecoratorBase, "impl")
        metas: dict[str, PromptDecoratorInfo] = {}
        for t in types:
            name: str = t.__name__
            d: PromptDecoratorBase = t.__new__(t)
            key: str = d.static_key()
            meta = PromptDecoratorInfo(key=key, plain_name=d.plain_name(), type=t, doc=t.__doc__)
            metas[key] = meta
        return metas

    def get_all_prompt_decorator_meta(self) -> list[PromptDecoratorInfo]:
        return [v for k, v in sorted(self.prompt_decorator_meta.items())]

    def get_all_prompt_decorator_keys(self) -> list[str]:
        return [m.key for m in self.get_all_prompt_decorator_meta()]

    def create_prompt_decorator_instance(self, d_key: str) -> PromptDecoratorBase:
        """
        Creates an instance of a prompt decorator in default settings by its key.
        :param d_key:
        :return:
        """
        info: PromptDecoratorInfo = self.prompt_decorator_meta.get(d_key, None)
        if info is None:
            raise ValueError(f"PromptDecorator with key '{d_key}' not found.")
        t = info.type
        pd: PromptDecoratorBase = t.__new__(t)
        pd = pd.create_default_instance(self.repository)
        # pd.__init__()
        return pd

    # endregion


if __name__ == "__main__":

    factory = PromptingFactory(InMemoryPromptRepository())
    print("\n")
    print("Prompting.Meta", factory.get_all_prompting_meta())
    print("Prompting.Keys", factory.get_all_prompting_keys())

    # Decorators
    print("\n")
    print("PromptDecorator.Meta", factory.get_all_prompt_decorator_meta())
    print("PromptDecorator.Keys", factory.get_all_prompt_decorator_keys())
