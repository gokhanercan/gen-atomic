from antlr4 import *
import builtins
import sys

from SQLiteLexer import SQLiteLexer
from SQLiteParser import SQLiteParser

def main():
    # Read input from a file
    print(dir(builtins))
    input_stream = FileStream('input.txt')

    try:
        lexer = SQLiteLexer(input_stream)
        stream = CommonTokenStream(lexer)
        parser = SQLiteParser(stream)
        tree = parser.parse()

        # Implement logic to traverse the parse tree and extract information
        print("SQL statement parsed successfully!")
    except RecognitionException as e:
        print(f"Error parsing SQL statement: {e}")


if __name__ == '__main__':
    main()
