import pprint
from typing import Iterable


def Print(label:str, obj):
    labelBold = f"\n\033[1m{label}\033[0m:"
    print(labelBold)
    pprint.pprint(obj)

def PrintObj(obj):
    if(isinstance(obj, Iterable)):
        Print(f"Iterable ({__get_iterable_type_name(obj)})", obj)
    else:
        Print(str(obj),obj)

def __get_iterable_type_name(iterable):
    if not isinstance(iterable, Iterable):
        return "Not an iterable"
    try:
        iterator = iter(iterable)
        first_element = next(iterator)
        return type(first_element).__name__
    except StopIteration:
        return "Empty iterable"