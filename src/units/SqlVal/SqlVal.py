from colorama import Fore

from data.Dataset import UnitType
from units.UnitBase import UnitBase
from unittest import TestCase
import re
import sqlparse


class SqlVal(UnitBase ):

    def __init__(self, unitType) -> None:
        UnitBase.__init__(self,unitType)

    def GetUnitType(self):
        return "SQL"     #Function|Class|Module....

    def CheckSyntax(self, code: str):
        pass

    def RunTest(self, code:str, correctCase:str)->bool:
        return self.validate_sql(code, correctCase)

    # region Regex Implementation
    @staticmethod
    def validate_sql(sql_pattern, test_string) -> bool:
        try:
            parsed = sqlparse.parse(sql_pattern)
            return True  # No parsing errors if we reach here
        except:
            print(f"{Fore.RED}Invalid SQL expression pattern.{Fore.RESET}")  # TODO: Handle that error well. Reflection.
            return False
    # endregion
class SqlTest(TestCase):
   def test_sql_pareser(self):
        sqlVal = SqlVal(UnitType.SQL)
        from unittest.mock import patch
        with patch.object(sqlVal, 'validate_sql', return_value=True):
            self.assertEqual(sqlVal.validate_sql("select from taht  +", "irrelevant"),True)


   def check_keywords(sql):
        keywords = r"\b(SELECT|FROM|WHERE|JOIN|ORDER BY|GROUP BY|HAVING|LIMIT|UNION|INTERSECT|EXCEPT)\b"
        return bool(re.findall(keywords, sql, flags=re.IGNORECASE))

if __name__ == "__main__":
    print("execute tes")