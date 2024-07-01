from typing import List

from colorama import Fore

from data.Dataset import UnitType, Condition
from units.UnitBase import UnitBase
from unittest import TestCase
import re
import sqlparse


class Sql(UnitBase):

    def __init__(self, unitType) -> None:
        UnitBase.__init__(self,unitType)

    # def GetUnitType(self):      #???
    #     return "SQLSelect"

    def CheckSyntax(self, code: str):       #Static check. Parse, SyntaxCheck, Compile.
        #ANTLR
        pass

    def RunTest(self, code:str, correctCase:str, conditions:List[Condition])->bool:
        import sqlite3
        #TODO: Pass schema and data context here.

        # Define the database schema
        schema = """
        CREATE TABLE IF NOT EXISTS products (
            ID INTEGER PRIMARY KEY,
            Name TEXT NOT NULL
        );
        """

        try:
            with sqlite3.connect(':memory:') as connection:
                #Schema
                cursor = connection.cursor()
                cursor.executescript(schema)
                connection.commit()

                #Data
                cursor.execute("INSERT INTO products (ID, Name) VALUES (?, ?)", (1,"Product1"))
                cursor.execute("INSERT INTO products (ID, Name) VALUES (?, ?)", (2,"A101"))
                connection.commit()

                #Query
                cursor.execute(code)
                resultset = cursor.fetchall()
                for row in resultset:
                    print(row)

        except sqlite3.Error as e:
            print(f"An error occurred: {e}")

        #EVAL
        passCount:int = 0
        for c in conditions:
            if(c.Criteria.name == "data-count"):
                datacount:int = len(resultset)
                passed:bool = datacount == int(c.Criteria.value)
                if(passed): passCount = passCount+1

        return passCount == len(conditions)


    @staticmethod
    def validate_sql(sql_pattern, test_string) -> bool:
        try:
            parsed = sqlparse.parse(sql_pattern)
            return True
        except:
            print(f"{Fore.RED}Invalid SQL expression pattern.{Fore.RESET}")  # TODO: Handle that error well. Reflection.
            return False

class SqlTest(TestCase):
   def test_sql_parser(self):
        #sql:UnitBase = Sql(UnitType.SQL)
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

