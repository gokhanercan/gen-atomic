import pkgutil
import importlib
import inspect
import sys
from abc import ABC
from utility.Paths import Paths
from utility.PrintHelper import *

sys.path.append(Paths().GetSourceRoot())        #We want to make sure that our SourceRoot is in the sys.paths for module/type discovery. That makes discovery caller path independent.

def find_subclasses(module_name:str, base_class, submoduleName:str = None)->set:
    subclasses = set()
    module = importlib.import_module(module_name)       #this is consumer's path dependant.
    for _, name, is_pkg in pkgutil.walk_packages(module.__path__, module.__name__ + "."):
        if not is_pkg:
            sub_module = importlib.import_module(name)
            for name, obj in inspect.getmembers(sub_module, inspect.isclass):
                if issubclass(obj, base_class) and obj is not base_class:
                    if (sub_module == submoduleName):       #filter by submodule
                        subclasses.add(obj)
                        continue
                    else:
                        subclasses.add(obj)
    return subclasses


if __name__ == '__main__':
    PrintObj(find_subclasses('models', ABC,'providers'))
