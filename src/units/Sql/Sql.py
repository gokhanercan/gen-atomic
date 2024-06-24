from typing import List

from colorama import Fore

from data.Dataset import UnitType, Condition
from units.UnitBase import UnitBase
from unittest import TestCase
import re
import sqlparse
import ast


class Sql(UnitBase):

    def __init__(self, unitType) -> None:
        UnitBase.__init__(self,unitType)

    # def GetUnitType(self):      #???
    #     return "SQLSelect"

    def CheckSyntax(self, code: str):       #Static check. Parse, SyntaxCheck, Compile.
        #ANTLR
        pass

    def createSchema(self, schema_str) -> str:
        table_name, columns = schema_str.split('(')
        table_name = table_name.strip()

        # Extracting column names
        columns = columns.replace(')', '')  # Remove the closing parenthesis
        column_list = columns.split(',')
        column_names = []
        column_type_dict = {}
        primary_key = None
        for column in column_list:
            column_name, column_type = column.split(':')
            if column_name.__contains__('*'):
                column_name = column_name.split('*')[0].strip()
                primary_key = column_name
            column_type_dict[column_name] = column_type
            column_names.append(column_name)

        # Identifying the primary key column
        if primary_key is None:
            primary_key = ''

        column_names = [column.split('*')[0].strip() if '*' in column else column.strip() for column in column_names]

        # Define the database schema
        schema = f"""CREATE TABLE IF NOT EXISTS {table_name} ("""

        for column_name in column_names:
            if column_name == primary_key:
                schema += f"{column_name} {column_type_dict[column_name]} PRIMARY KEY, "
            else:
                schema += f"{column_name} {column_type_dict[column_name]}, "
        schema = schema[:-2] + ");"

        return schema, column_names, column_type_dict, table_name

    def createData(self, data_str, column_names, column_type_dict) -> List[tuple]:
        # Step 1: Clean the string to remove unwanted characters
        data_str_cleaned = data_str.strip('{[]}').replace("'", "")

        # Step 2: Split the string into individual data entries
        entries = data_str_cleaned.split('},{')

        # Step 3: Parse each entry and convert to the desired format
        result = []
        for entry in entries:
            # Remove any remaining braces
            entry = entry.strip('{}')
            # Split the entry into key-value pairs
            pairs = entry.split(',')

            # Extract values in the order of column_names
            values = []
            for col in column_names:
                for pair in pairs:
                    key, value = pair.split(':')
                    if key == col:
                        # Convert the value to the appropriate type
                        if column_type_dict[col] == 'INTEGER':
                            values.append(int(value))
                        elif column_type_dict[col] == 'FLOAT':
                            values.append(float(value))
                        elif column_type_dict[col] == 'VARCHAR':
                            values.append(value)
                        break

            # Convert the list of values to a tuple
            result.append(tuple(values))

            return result

    def RunTest(self, code:str, correctCase:str, conditions:List[Condition])->bool:
        import sqlite3

        data_str = "{[{ID:1,Name:'Product1',Price:10},{ID:2,Name:'AnotherProduct2',Price:20}]}"

        #string split operations
        schema_str = "Products(ID*:INTEGER,Name:VARCHAR,Price:FLOAT)"

        schema, column_names, column_type_dict, table_name = self.createSchema(schema_str)

        result = self.createData(data_str, column_names, column_type_dict)


        try:
            with sqlite3.connect(':memory:') as connection:
                #Schema
                cursor = connection.cursor()
                cursor.executescript(schema)
                connection.commit()
                insert_statement = f"INSERT INTO {table_name} ({', '.join(column_names)}) VALUES ({', '.join(['?'] * len(column_names))})"

                for row in result:
                    cursor.execute(insert_statement, row)

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

    def getPrompt(self, description) -> str:
        instruction:str = ("Consider yourself a function that takes the input of asked validation sql statement, and "
                           "your output should be a markdown code snippet formatted in the following schema, including "
                           "the leading and trailing \"```sql\" and \"```\". Do not give me an explanation, only give "
                           "me a sql expression. Do not add any additional characters.")
        prompt:str = f"{instruction}\nAsked sql statement: {description}."
        promptColored: str = f"{instruction}\nAsked sql statement: {Fore.BLUE}{description}{Fore.RESET}."
        print(f"\nP:{promptColored}")
        print(Fore.RESET)

        return prompt

    def parseOutput(self, answer) -> str:
        sql_pattern = r"```sql(.*?)```"
        match = re.search(sql_pattern, answer, re.DOTALL)  # re.DOTALL allows matching newlines

        print(f"Full Output:\n{answer}\n")

        if match:

            extracted_sql = match.group(1)
            print(f"Extracted sql pattern: {Fore.CYAN}{extracted_sql}{Fore.RESET}")
            return extracted_sql.strip()
        else:
            print("Couldn't find sql pattern between ```")
            return answer


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
    p = sqlparse.parse("select ! from (SELECT * from PRODUCTS) as p)")
    for stmt in p:
        print(stmt._pprint_tree())

    #print("execute tes")

