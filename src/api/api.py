from typing import List
import meta
from langunits.LangUnitFactory import LangUnitFactory
from models.ModelFactory import ModelFactory
from prompting.prompting_factory import PromptingFactory
from utility.PrintHelper import *
from meta import __version__


# noinspection PyMethodMayBeStatic
class API(object):
    """
    Library-level Facade API layer (not an endpoint) for easily interacting with the library.
    """

    def __init__(self) -> None:
        super().__init__()
        self.app = FastAPI()

    def GetAllLangUnitNames(self) -> List[str]:
        return LangUnitFactory().GetAllLangUnitNames()

    def GetAllModelProviderNames(self) -> List[str]:
        return ModelFactory().GetAllModelProviderNames()

    def GetAllModelKeys(self) -> List[str]:
        return ModelFactory().GetAllModelKeys()

    def get_all_prompting_keys(self) -> List[str]:
        return PromptingFactory().get_all_prompting_keys()

    def get_all_prompt_decorator_keys(self) -> List[str]:
        return PromptingFactory().get_all_prompt_decorator_keys()

    def get_version(self) -> str:
        return __version__

    def get_version_on_platform(self) -> str:
        return meta.get_version_on_platform()


# region fast api
from fastapi import FastAPI

api: API = API()
app = FastAPI(
    title="genatomic-api",
    description="gen-atomic fastapi implementation",
    version=api.get_version(),
)


@app.get("/version")
def get_version() -> str:
    return api.get_version()


@app.get("/version_badge")
def get_version_badge():
    return {
        "schemaVersion": 1,
        "label": "version",
        "message": "v" + api.get_version(),
        "color": "blue",
    }


# endregion


if __name__ == "__main__":
    api = API()
    Print("Version", api.get_version())
    Print("VersionOnPlatform", api.get_version_on_platform())
    print("-" * 50)
    Print("ModelProviders", api.GetAllModelProviderNames())
    Print("ModelKeys", api.GetAllModelKeys())
    Print("PromptingKeys", api.get_all_prompting_keys())
    Print("PromptDecorators", api.get_all_prompt_decorator_keys())
