from colorama import Fore

from data.Dataset import UnitType
from units.UnitBase import UnitBase
from unittest import TestCase
import re
import sqlparse


class Sql(UnitBase):

    def __init__(self, unitType) -> None:
        UnitBase.__init__(self,unitType)

    def GetUnitType(self):
        return "SQL"

    def CheckSyntax(self, code: str):       #Static check. Parse, SyntaxCheck, Compile.
        #ANTLR
        pass

    def RunTest(self, code:str, correctCase:str)->bool:
        # cond1="data-count=2"
        # data = new SQlLite("db schema").Init().Run("lln gen query")
        # if("data-count"):   #
        #     cond1.val("data-count") == len(data)
        return self.validate_sql(code, correctCase)

    # region Regex Implementation
    @staticmethod
    def validate_sql(sql_pattern, test_string) -> bool:
        try:
            parsed = sqlparse.parse(sql_pattern)
            return True
        except:
            print(f"{Fore.RED}Invalid SQL expression pattern.{Fore.RESET}")  # TODO: Handle that error well. Reflection.
            return False
    # endregion
class SqlTest(TestCase):
   def test_sql_parser(self):
        sql:UnitBase = Sql(UnitType.SQL)
        from unittest.mock import patch
        # with patch.object(sqlVal, 'validate_sql', return_value=True):
        #     self.assertEqual(sqlVal.validate_sql("saFDDSDFSDFDSFDS AA taht  +", "irrelevant"),True)


   def check_keywords(sql):
        keywords = r"\b(SELECT|FROM|WHERE|JOIN|ORDER BY|GROUP BY|HAVING|LIMIT|UNION|INTERSECT|EXCEPT)\b"
        return bool(re.findall(keywords, sql, flags=re.IGNORECASE))

if __name__ == "__main__":
    p = sqlparse.parse("select ! from (SELECT * from PRODUCT) as p)")
    for stmt in p:
        print(stmt._pprint_tree())

    #print("execute tes")

