import importlib
import inspect
import os
from typing import Dict, Type, Tuple
from antlr4 import Parser, Lexer, FileStream, CommonTokenStream, RecognitionException, InputStream

from AntlrWrapper import AntlrWrapper
from utility.Paths import Paths

class AntlrParserDiscovery(object):

    def __init__(self, autoDiscover:bool = True) -> None:
        super().__init__()
        self.AutoDiscover:bool = autoDiscover
        self.Tuples:Dict[str,Tuple[Type, Type]] = {}
        if(self.AutoDiscover):
            self.Tuples = self.DiscoverParserTypes()

    def CreateAntlrParser(self, grammarName:str, input:str)->AntlrWrapper:
        tuple = self.Tuples[grammarName]
        input_stream = InputStream(input)
        lexerType = tuple[0]
        parserType = tuple[1]
        lexerInstance:Lexer = lexerType.__new__(lexerType)
        lexerInstance.__init__(input_stream)
        stream = CommonTokenStream(lexerInstance)
        parserInstance:Parser = parserType.__new__(parserType)
        parserInstance.__init__(stream)
        return AntlrWrapper(parserInstance)

    def DiscoverParserTypes(self) -> Dict[str,Tuple[Type, Type]]:     #GrammarName | <Lexer|Parser>
        projectRootPath:str = Paths().GetProjectRoot()
        tuples: Dict[str, Tuple[Type, Type]] = {}

        #Lexer
        lexerTypes = self.discover_subclasses_in_project(Lexer, projectRootPath)
        for lexerType in lexerTypes:
            grammarName:str = lexerType.__name__.replace("Lexer","")
            tuples[grammarName] = (lexerType,lexerType)

        #Parser
        parserTypes = self.discover_subclasses_in_project(Parser, projectRootPath)
        for parserType in parserTypes:
            grammarName: str = parserType.__name__.replace("Parser", "")
            tuple = tuples[grammarName]
            if(tuple is not None):
                tuple = (tuple[0],parserType)
                tuples[grammarName] = tuple
        return tuples

    #region Discovery Impl
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
    #endregion

if __name__ == '__main__':
    discovery = AntlrParserDiscovery(True)
    tuples = discovery.DiscoverParserTypes()
    print(tuples)
    print(discovery.CreateAntlrParser("SQLite","select * from Products").Parse())
    print(discovery.CreateAntlrParser("SQLite","select111 * from Products").Parse())