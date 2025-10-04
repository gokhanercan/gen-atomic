from models.ModelBase import *
from models.providers.ModelProviderBase import ModelProviderBase
from utility import Discovery
from utility.PrintHelper import Print


@dataclass
class ModelFilters:
    provider_abbr: str = None
    provider_name: str = None
    key_contains: str = None
    is_baseline: Optional[bool] = None


class ModelFactory(object):
    def __init__(self) -> None:
        super().__init__()

        self._standalone_meta: dict[str, StandaloneModelMeta] | None = None
        self._provider_meta: dict[str, ModelProviderMeta] | None = None
        self._model_index: dict[str, ModelMeta] | None = None

    @property
    def standalone_models_meta(self) -> dict[str, StandaloneModelMeta]:
        if self._standalone_meta is None:
            self._standalone_meta = self._discover_standalone_models()
        return self._standalone_meta

    @property
    def model_providers_meta(self) -> dict[str, ModelProviderMeta]:
        if self._provider_meta is None:
            self._provider_meta = self._discover_model_providers()
        return self._provider_meta

    @property
    def model_index(self) -> dict[str, ModelMeta]:
        if self._model_index is None:
            self._model_index = self._build_model_index()
        return self._model_index

    def _build_model_index(self) -> dict[str, ModelMeta]:
        index: dict[str:ModelMeta] = {}

        # Standalone ones
        for k, v in self.standalone_models_meta.items():
            s_meta: StandaloneModelMeta = v
            s_model: ModelBase = self.create_model(s_meta.name)
            key: str = s_model.key()
            meta: ModelMeta = ModelMeta(
                name=s_meta.name,
                plain_name=s_model.plain_name(),
                key=key,
                standalone_model_meta=s_meta,
                model_provider_meta=None,
            )
            index[key] = meta
            s_model.model_meta = meta

        # Provider Models
        for k, v in self.model_providers_meta.items():
            mp_meta: ModelProviderMeta = v
            models: List[ModelBase] = self.create_models_by_provider(mp_meta.name)
            for m in models:
                key: str = m.key()
                meta: ModelMeta = ModelMeta(
                    name=m.name(),
                    plain_name=m.plain_name(),
                    key=key,
                    standalone_model_meta=None,
                    model_provider_meta=mp_meta,
                )
                index[key] = meta
                m.model_meta = meta
        return index

    # region Model Instance Creators
    def create_model_by_key(self, key: str) -> ModelBase:
        meta: ModelMeta = self.model_index[key]
        if meta.is_standalone:
            m: ModelBase = self.create_model(meta.name, meta)
            return m
        else:
            mp: ModelProviderBase = self.create_model_provider(meta.model_provider_meta.name, meta.plain_name)
            return mp

    def find_keys_by_filters(self, mf: ModelFilters):
        filtered: dict[str, ModelMeta] = self.model_index

        # region Apply filters
        def filter_provider_abbr(filter: str, meta: ModelMeta):
            return filter == meta.key.split(".")[0]

        def filter_provider_name(filter: str, meta: ModelMeta):
            if meta.model_provider_meta:
                return filter == meta.model_provider_meta.name
            return False

        def filter_key_contains(filter: str, meta: ModelMeta):
            return meta.key.__contains__(filter)

        # endregion

        if mf.provider_abbr:
            filtered = {k: v for k, v in filtered.items() if filter_provider_abbr(mf.provider_abbr, v)}
        if mf.provider_name:
            filtered = {k: v for k, v in filtered.items() if filter_provider_name(mf.provider_name, v)}
        if mf.key_contains:
            filtered = {k: v for k, v in filtered.items() if filter_key_contains(mf.key_contains, v)}
        if mf.is_baseline:
            filtered = {k: v for k, v in filtered.items() if v.is_baseline == mf.is_baseline}

        return filtered

    def create_models_by_filters(self, mf: ModelFilters) -> List[ModelBase]:
        filtered: dict[str, ModelMeta] = self.find_keys_by_filters(mf)
        return [self.create_model_by_key(k) for k, v in filtered.items()]

    def create_all_models(self) -> List[ModelBase]:
        return [self.create_model_by_key(k) for k, v in self.model_index.items()]

    def create_standalone_models(self) -> List[ModelBase]:
        models: List[ModelBase] = []
        for model_name in self.get_all_standalone_model_names():
            m: ModelBase = self.create_model(model_name)
            models.append(m)
        return models

    def create_baseline_models(self) -> List[ModelBase]:
        models: List[ModelBase] = []
        for model_name in self.get_all_baseline_model_names():
            m: ModelBase = self.create_model(model_name)
            models.append(m)
        return models

    def create_model_providers(self) -> List[ModelProviderBase]:
        providers: List[ModelProviderBase] = []
        for mp_name in self.get_all_model_provider_names():
            mp: ModelProviderBase = self.create_model_provider(mp_name)
            providers.append(mp)
        return providers

    def create_model_provider(self, provider_name: str, model_name: Optional[str] = None) -> ModelProviderBase:
        t: ABCMeta = self.model_providers_meta[provider_name].type
        mp: ModelProviderBase = t.__new__(t)
        mp.__init__(model_name)
        return mp

    def create_models_by_provider(self, provider_name: str) -> List[ModelProviderBase]:
        p: ModelProviderBase = self.create_model_provider(provider_name)
        model_names = p.model_names()
        mps: List[ModelProviderBase] = []
        for model_name in model_names:
            mp: ModelProviderBase = self.create_model_provider(provider_name, model_name)
            mps.append(mp)
        return mps

    def create_model(self, model_name: str, model_meta: ModelMeta | None = None) -> ModelBase:
        t: ABCMeta = self.standalone_models_meta[model_name].type
        m: ModelBase = t.__new__(t)
        m.__init__()
        if model_meta:
            m.model_meta = model_meta
        return m

    # endregion

    # region Queries

    def get_all_model_provider_names(self) -> List[str]:
        return [k for k in self.model_providers_meta]

    def get_all_model_provider_infos(self) -> List[ModelProviderMeta]:
        return [v for k, v in self.model_providers_meta.items()]

    def get_all_standalone_model_names(self) -> List[str]:
        return [k for k in self.standalone_models_meta]

    def get_all_baseline_model_names(self) -> List[str]:
        return [
            key for key, value in self.standalone_models_meta.items() if value.is_baseline == True
        ]  # Limited to standalone models only for now.

    def get_all_model_keys(self) -> List[str]:
        return [k for k, v in self.model_index.items()]

    def get_model_keys(
        self, baseline_filter: Optional[bool] = None
    ) -> List[str]:  # TODO: add more filters here. ExcludeBaselines, FilterByModelName, ByProviderName etc.
        return [k for k, v in self.model_index.items() if v.is_baseline == baseline_filter and baseline_filter is not None]

    # endregion

    # region Discovery
    @staticmethod
    def _discover_baseline_models() -> dict[str, StandaloneModelMeta]:
        """
        Lists all available baseline model names
        :return:
        """
        return {k: v for k, v in ModelFactory._discover_standalone_models().items() if v.is_baseline}

    @staticmethod
    def _discover_standalone_models() -> dict[str, StandaloneModelMeta]:
        """
        Discovers standalone models, not server through model providers
        :return:
        """
        types = Discovery.find_subclasses(
            "models", ModelBase
        )  # TODO: It can be in any module when it is a plugin. Remove that criteria
        metas: dict[str, StandaloneModelMeta] = {}
        for t in types:
            name: str = t.__name__
            is_baseline: bool = issubclass(t, BaselineModel)
            if issubclass(t, ModelProviderBase):
                continue  # Skipping non-standalone models here. They are discovered in a separate process
            meta = StandaloneModelMeta(name, t, is_baseline)
            metas[name] = meta
        return metas

    @staticmethod
    def _discover_model_providers() -> dict[str, ModelProviderMeta]:
        types = Discovery.find_subclasses("models", ModelProviderBase, "providers")
        metas: dict[str, ModelProviderMeta] = {}
        for t in types:
            name: str = t.__name__
            mp: ModelProviderBase = t.__new__(t)
            mp.__init__()
            meta = ModelProviderMeta(name, t, mp.provider_abbreviation())
            metas[name] = meta
        return metas

    # endregion


if __name__ == "__main__":
    # STATIC Discovery
    Print("BaselineModelsMeta", ModelFactory._discover_baseline_models())
    Print("StandaloneModelsMeta", ModelFactory._discover_standalone_models())
    Print("ModelProvidersMeta", ModelFactory._discover_model_providers())

    # INSTANCE Queries
    factory = ModelFactory()
    Print("ModelProviderNames", factory.get_all_model_provider_names())
    Print("StandaloneModelNames", factory.get_all_standalone_model_names())
    Print("BaselineModelNames", factory.get_all_baseline_model_names())

    # Keys
    Print("ModelIndex", factory.model_index)
    Print("AllModelKeys", factory.get_all_model_keys())
    Print(
        "FindKeysByFilters usage", factory.FindKeysByFilters(ModelFilters("ol", "OllamaModelProvider", "llama3", False))
    )

    # Models Instance Creation
    Print("BaselineModels", factory.CreateBaselineModels())
    Print("StandaloneModels", factory.CreateStandaloneModels())
    Print("ModelProviders", factory.CreateModelProviders())
    Print("AllEffectiveModels", factory.CreateAllModels())
    Print(
        "CreateModelsByFilters() usage",
        factory.CreateModelsByFilters(ModelFilters("ol", "OllamaModelProvider", "llama", False)),
    )

    # usages
    Print("CreateModel(name) usage", factory.CreateModel("RandomModel"))
    Print("CreateModelProvider(name) usage", factory.CreateModelProvider("OllamaModelProvider"))
    Print("CreateModelsByProvider(name) usage", factory.CreateModelsByProvider("OllamaModelProvider"))
    Print("CreateModelByKey(key) usage via standalones", factory.CreateModelByKey("np.random"))
    Print("CreateModelByKey(key) usage via providers", factory.CreateModelByKey("ol.codellama"))
