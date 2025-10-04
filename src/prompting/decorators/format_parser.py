from abc import ABC, abstractmethod

from models.ModelBase import GenResponse


class FormatParserBase(ABC):

    @abstractmethod
    def parse(self, res: GenResponse) -> GenResponse:
        """
        Parses the given raw generated text and returns a new instance of GenResponse with the parsed content.
        """
        pass
