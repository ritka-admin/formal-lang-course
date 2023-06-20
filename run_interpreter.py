import sys
import shared
from antlr4 import *

from language.antlr_gen.LaLaLangParser import LaLaLangParser
from language.antlr_gen.LaLaLangLexer import LaLaLangLexer
from project.interpreter import Interpreter


if __name__ == "__main__":
    expr = FileStream(sys.argv[1])
    lexer = LaLaLangLexer(expr)
    stream = CommonTokenStream(lexer)
    parser = LaLaLangParser(stream)
    tree = parser.program()
    interpreter = Interpreter(tree)
    if interpreter.interpret():
        print(interpreter.interpret())

