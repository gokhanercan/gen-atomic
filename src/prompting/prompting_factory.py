from prompting.PromptingBase import PromptingInfo, PromptingBase
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
            # p.__init__()      #we don't need to call __init__ here, as we are creating static metadata only.
            key:str = p.key()
            meta = PromptingInfo(key=key, plain_name=p.plain_name(), type=t, doc=t.__doc__)
            metas[key] = meta
        return metas

    def get_all_prompting_meta(self) -> list[PromptingInfo]:
        return [v for k,v in self.promptings_meta.items()]

    def get_all_prompting_keys(self) -> list[str]:
        return [m.key for m in self.get_all_prompting_meta()]


if __name__ == '__main__':

    factory = PromptingFactory()
    print("PromptingFactory", factory.promptings_meta)
    print("meta",factory.get_all_prompting_meta())
    print("keys",factory.get_all_prompting_keys())