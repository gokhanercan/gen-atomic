import unittest
from unittest import TestCase


class FormatHelper(object):

    @staticmethod
    def ShortenCode(code:str, middleTrim:int = 0):
        if (middleTrim > 0):
            if (len(code) > middleTrim * 2):
                code = FormatHelper.TrimMiddle(code,middleTrim)
        formatted = f"[CODE] {code} [/CODE]"
        return formatted

    @staticmethod
    def TrimMiddle(str:str, nSides)->str:
        end_index = len(str) - nSides
        trimmed_string = str[:nSides] + " ..[TRIM].. " + str[end_index:]
        return trimmed_string


class FormatHelperTest(TestCase):
    def test_ShortenCode_SmallCodeWith50TrimSize_DoNotTouch(self):
        self.assertEqual("[CODE] var x = 100; [/CODE]", FormatHelper.ShortenCode("var x = 100;",50))

if __name__ == "__main__":
    unittest.main()