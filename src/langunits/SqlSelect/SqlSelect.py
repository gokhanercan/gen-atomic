from typing import List
from data.Dataset import Unit
from langunits.LangUnit import LangUnit, UnitType


class SqlSelect(LangUnit):
    def __init__(self) -> None:
        super().__init__()
        LangUnit.__init__()
    def PromptText(self):
        return "SQL select query"

    def GetUnitType(self) -> UnitType:
        return UnitType.Query

    def CheckSyntax(self, code: str):       #Static check. Parse, SyntaxCheck, Compile.
        #ANTLR
        pass

    #region Internal Impl
    def createSchema(self, schema_str):
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
    #endregion

    def RunTest(self, code:str, correctCase:str, unit:Unit)->bool:
        import sqlite3
        schema, column_names, column_type_dict, table_name = self.createSchema(unit.Context.Schema)
        result = self.createData(unit.Context.Data, column_names, column_type_dict)

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
            return False

        #EVAL
        passCount:int = 0
        for c in unit.Constraints:
            name,value = c.Criteria.name,c.Criteria.value
            if(name == "data-count"):
                datacount:int = 0 if resultset is None else len(resultset)
                passed:bool = datacount == int(value)
                if(passed): passCount = passCount+1

        return passCount == len(unit.Constraints)