from abc import ABCMeta

from langunits.LangUnit import LangUnitInfo
from prompting.PromptingBase import PromptingInfo, PromptingBase
from prompting.impl.DirectPrompting import DirectPrompting
from utility import Discovery


class PromptingFactory(object):

    def __init__(self) -> None:
        super().__init__()
        self.promptings_meta: dict[str, PromptingInfo] = self.discover_promptings()

    def discover_promptings(self) -> dict[str, PromptingInfo]:
        types = Discovery.find_subclasses("prompting",PromptingBase,"impl")
        metas: dict[str, PromptingInfo] = {}
        for t in types:
            name: str = t.__name__
            p: PromptingBase = t.__new__(t)
            key:str = p.static_key()    # TODO: static or dynamic key?
            meta = PromptingInfo(key=key, plain_name=p.plain_name(), type=t, doc=t.__doc__)
            metas[key] = meta
        return metas

    def get_all_prompting_meta(self) -> list[PromptingInfo]:
        return [v for k,v in self.promptings_meta.items()]

    def get_all_prompting_keys(self) -> list[str]:
        return [m.key for m in self.get_all_prompting_meta()]

    def create_default(self, lang_unit_name:str) -> PromptingBase:
        return DirectPrompting("p1")     #TODO: Load pid per langunit and model here

    def create_direct_prompt(self, pid:str) -> PromptingBase:
        return DirectPrompting(pid)

    def create_prompting_instance(self, p_key:str, lang_unit_info:LangUnitInfo) -> PromptingBase:
        info:PromptingInfo = self.promptings_meta.get(p_key, None)
        if(info is None):
            raise ValueError(f"Prompting with key '{p_key}' not found.")

        t = info.type      #TODO: This Type is MetaABC in ModelFactory, but throws error here. Why?
        p: PromptingBase = t.__new__(t)
        if (t != type(p)):
            raise TypeError(f"Type mismatch: Expected {t}, got {type(p)}")
        p = p.create_default_instance(lang_unit_info)
        return p


if __name__ == '__main__':

    factory = PromptingFactory()
    print("PromptingFactory", factory.promptings_meta)
    print("meta",factory.get_all_prompting_meta())
    print("keys",factory.get_all_prompting_keys())