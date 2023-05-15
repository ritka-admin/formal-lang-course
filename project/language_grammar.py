import sys
from antlr4 import *

from language.antlr_gen.LaLaLangParser import LaLaLangParser
from language.antlr_gen.LaLaLangLexer import LaLaLangLexer


def grammar(arg: str):
    # inp = StdinStream(encoding="utf-8")
    inp = InputStream('var x = )5')
    lexer = LaLaLangLexer(inp)
    stream = CommonTokenStream(lexer)
    parser = LaLaLangParser(stream)
    tree = parser.program()
    print("lol")


if __name__ == '__main__':
    grammar('var x = 5;')
