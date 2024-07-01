import dataclasses

from antlrValidation.AntlrParserFactory import AntlrParserFactory


@dataclasses
class ParseResult(object):
    IsParsed:bool
    ParseError:Exception
    ParseDurationInMs:int

class AntlrWrapper(object):     #Base:Parsers/SyntaxCheckers.

    def Parse(self, grammarName:str, input:str)->ParseResult:      #TODO:Return Complex type
        parserType = AntlrParserFactory().DiscoverParser(grammarName)
        #parser.parse       -> main.
        return ParseResult()

if __name__ == '__main__':

    AntlrWrapper().Parse("SQ",   "select * from Table")
    AntlrWrapper().Parse("HTML", "<input>")
    AntlrWrapper().Parse("JSON", "[]{myjson:'sda'}")