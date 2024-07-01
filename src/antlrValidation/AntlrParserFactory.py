import importlib
import inspect
import os
from typing import Dict
from antlr4 import Parser, Lexer, FileStream, CommonTokenStream, RecognitionException
from utility.Paths import Paths

class AntlrParserFactory(object):

    def __init__(self) -> None:
        super().__init__()

    #def CreateParserWithInput(grammarName,input)  create instance with input data.

    def DiscoverParser(self, grammarName: str) -> Parser:
        dict = self.DiscoverParsers()
        return dict[grammarName]

    def DiscoverParsers(self) -> Dict[str, Parser]:     #TODO: Return Lexer|Parser type tuple.
        parsers:Dict[str,Parser] = {}
        projectRootPath:str = Paths().GetProjectRoot()

        #Lexer
        lexerTypes = self.discover_subclasses_in_project(Lexer, projectRootPath)
        for lexerType in lexerTypes:
            if(str(lexerType.__name__).__contains__("Expr")): continue
            print(f"Found subclass: {lexerType.__name__}")
            #TODO: load from file path.
            input_stream = FileStream('L:\\Projects\\gen-atomic\\src\\antlrValidation\\sqlCK\\input.txt')
            lexerInstance:Lexer = lexerType.__new__(lexerType)
            lexerInstance.__init__(input_stream)
            stream = CommonTokenStream(lexerInstance)
            parserTypes = self.discover_subclasses_in_project(Parser, projectRootPath)
            for parserType in parserTypes:
                if (str(parserType.__name__).__contains__("Expr")): continue
                print(f"Found subclass: {parserType.__name__}")
                parserInstance:Parser = parserType.__new__(parserType)
                parserInstance.__init__(stream)
                grammarName:str = type(parserInstance).__name__.replace("Parser","")
                parsers[grammarName] = parserInstance
        return parsers

    def discover_subclasses_in_project(self,base_class, project_path):
        subclasses = []
        for root, _, files in os.walk(project_path):
            for file in files:
                if file.endswith(".py"):
                    file_path = os.path.join(root, file)
                    relative_path = os.path.relpath(file_path, project_path)
                    module = self.import_module_from_file(relative_path)
                    if module:
                        subclasses.extend(self.find_subclasses(base_class, module))
        return subclasses
    def find_subclasses(self,base_class, module):
        subclasses = []
        for name, obj in inspect.getmembers(module):
            if inspect.isclass(obj) and issubclass(obj, base_class) and obj is not base_class:
                subclasses.append(obj)
        return subclasses
    def import_module_from_file(self,filepath):
        module_name = filepath.replace('/', '.').replace('\\', '.').rstrip('.py')
        try:
            module = importlib.import_module(module_name)
            return module
        except ImportError:
            return None


if __name__ == '__main__':
    parser:Parser = AntlrParserFactory().DiscoverParser("SQLite")
    try:
        tree = parser.parse()
        print(tree)
        print("SUCCESS")
    except RecognitionException as e:
        print(f"Error parsing SQL statement: {e}")