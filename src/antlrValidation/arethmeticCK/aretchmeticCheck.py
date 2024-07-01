from antlr4 import *
import builtins
import sys



from ExprLexer import ExprLexer
from ExprParser import ExprParser

def main():
    # Read input from a file
    print(dir(builtins))
    input_stream = FileStream('input.txt')

    try:
        lexer = ExprLexer(input_stream)
        stream = CommonTokenStream(lexer)
        parser = ExprParser(stream)
        tree = parser.start_()

        # Implement logic to traverse the parse tree and extract information
        print("SQL statement parsed successfully!")
    except RecognitionException as e:
        print(f"Error aretchmetic statement: {e}")


if __name__ == '__main__':
    main()
