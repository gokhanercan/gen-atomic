from functools import reduce
from unittest import TestCase


def IsNullOrEmpty(str) -> bool:
    return not str

def IsNullOrWhiteSpace(str) -> bool:
    return str is None or len(str.strip()) == 0

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


    def test_IsNullOrWhiteSpace_DetectSingleWhitespace(self):
        self.assertTrue(IsNullOrWhiteSpace(" "))

    def test_IsNullOrWhiteSpace_DetectMultiplesWhitespaces(self):
        self.assertTrue(IsNullOrWhiteSpace("   "))