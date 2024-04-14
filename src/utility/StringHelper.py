from functools import reduce
from unittest import TestCase


def IsNullOrEmpty(str) -> bool:
    """
    Bu Helper yerine string'in not ile kontrol edebilirsin.
    :param str:
    :return:
    """
    # https://stackoverflow.com/questions/9573244/most-elegant-way-to-check-if-the-string-is-empty-in-python
    return not str


def Coelesce(*arg):
    """
    Modified to pass empty strings too
    ref: https://stackoverflow.com/questions/4978738/is-there-a-python-equivalent-of-the-c-sharp-null-coalescing-operator
    :param str:
    :param arg:
    :return:
    """
    return reduce(lambda x, y: x if not IsNullOrEmpty(x) else y, arg)


class StringHelperTest(TestCase):

    def test_Coelesce_PassNones(self):
        self.assertEqual("Null", Coelesce(None, "Null", None))

    def test_Coelesce_ChooseFirstStr(self):
        self.assertEqual("Str1", Coelesce("Str1", "Str2"))

    def test_Coelesce_PassEmpties(self):
        self.assertEqual("Str2", Coelesce("", "", "Str2", "Str3", "", "None"))
