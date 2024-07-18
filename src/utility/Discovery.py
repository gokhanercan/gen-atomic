from units.UnitBase import UnitBase


# class TypeDiscovery(object):
#
#     def __init__(self) -> None:
#         super().__init__()
#
#     def Discover(self):
#         pass
#
#     def get_subclasses(self,cls):
#         subclasses = set(cls.__subclasses__())
#         all_subclasses = set(subclasses)
#         for subclass in subclasses:
#             all_subclasses.update(self.get_subclasses(subclass))
#         return all_subclasses

import pkgutil
import importlib
import inspect


def find_subclasses(module_name, base_class):
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
    # print(TypeDiscovery().get_subclasses(UnitBase))
    print(find_subclasses('units', UnitBase))