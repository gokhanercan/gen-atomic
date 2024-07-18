import pkgutil
import importlib
import inspect
from abc import ABCMeta


def find_subclasses(module_name:str, base_class)->set:
    subclasses = set()
    module = importlib.import_module(module_name)
    for _, name, is_pkg in pkgutil.walk_packages(module.__path__, module.__name__ + "."):
        if not is_pkg:
            sub_module = importlib.import_module(name)
            for name, obj in inspect.getmembers(sub_module, inspect.isclass):
                if issubclass(obj, base_class) and obj is not base_class:
                    subclasses.add(obj)
    return subclasses


if __name__ == '__main__':
    print(find_subclasses('utility', ABCMeta))