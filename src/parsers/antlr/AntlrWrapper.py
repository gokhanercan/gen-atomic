from dataclasses import dataclass
from typing import Optional

from antlr4 import Parser, RecognitionException

@dataclass
class ParseResult(object):
    IsParsed:bool
    ParseError:Optional[Exception]

    @classmethod
    def Error(cls, error: Exception):
        return cls(IsParsed=False,ParseError=error)

class AntlrWrapper(object):
    def __init__(self, parser:Parser) -> None:
        super().__init__()
        self.Parser = parser

    def Parse(self)->ParseResult:
        try:
            tree = self.Parser.parse()
            if(tree.exception is None):
                return ParseResult(True,None)
            else:
                return ParseResult.Error(tree.exception)
        except Exception as e:
            return ParseResult.Error(e)

if __name__ == '__main__':
    pass