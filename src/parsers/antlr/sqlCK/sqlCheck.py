from antlr4 import *

from SQLiteLexer import SQLiteLexer
from SQLiteParser import SQLiteParser

def main():
    input_stream = FileStream('input.txt')
    try:
        lexer = SQLiteLexer(input_stream)
        stream = CommonTokenStream(lexer)
        parser = SQLiteParser(stream)
        tree = parser.parse()
        print("SQL statement parsed successfully!")
    except RecognitionException as e:
        print(f"Error parsing SQL statement: {e}")

if __name__ == '__main__':
    main()