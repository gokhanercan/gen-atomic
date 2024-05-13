from abc import ABC, abstractmethod


class ModelBase(ABC):
    def __init__(self) -> None:
        super().__init__()

    def ModelName(self):        #TODO: delete
        return str(type(self).__name__).replace("Model","")

    #@abstractmethod
    def ProviderName(self)->str:
        return "NoProvider"

    def ProviderAbbreviation(self)->str:
        return "NP"

    def ModelConfAbbr(self)->str:
        return f"{self.ProviderAbbreviation()}-{self.ModelName()}"

    @abstractmethod
    def Generate(self, description: str) -> str:
        pass