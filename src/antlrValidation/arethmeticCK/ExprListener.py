# Generated from Expr.g4 by ANTLR 4.13.1
from antlr4 import *
if "." in __name__:
    from .ExprParser import ExprParser
else:
    from ExprParser import ExprParser

# This class defines a complete listener for a parse tree produced by ExprParser.
class ExprListener(ParseTreeListener):

    # Enter a parse tree produced by ExprParser#start_.
    def enterStart_(self, ctx:ExprParser.Start_Context):
        pass

    # Exit a parse tree produced by ExprParser#start_.
    def exitStart_(self, ctx:ExprParser.Start_Context):
        pass


    # Enter a parse tree produced by ExprParser#expr.
    def enterExpr(self, ctx:ExprParser.ExprContext):
        pass

    # Exit a parse tree produced by ExprParser#expr.
    def exitExpr(self, ctx:ExprParser.ExprContext):
        pass


    # Enter a parse tree produced by ExprParser#atom.
    def enterAtom(self, ctx:ExprParser.AtomContext):
        pass

    # Exit a parse tree produced by ExprParser#atom.
    def exitAtom(self, ctx:ExprParser.AtomContext):
        pass



del ExprParser