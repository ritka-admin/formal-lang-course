import pytest
from antlr4 import *
from project.interpreter import Interpreter

from language.antlr_gen.LaLaLangParser import LaLaLangParser
from language.antlr_gen.LaLaLangLexer import LaLaLangLexer


def create_tree(stmt):
    expr = InputStream(stmt)
    lexer = LaLaLangLexer(expr)
    stream = CommonTokenStream(lexer)
    parser = LaLaLangParser(stream)
    tree = parser.program()
    return tree


@pytest.mark.parametrize('stmt', ['var x = false; print(x);',
                                  'print(5);', 'print("string");'])
def test_print_stmt(stmt):
    tree = create_tree(stmt)
    Interpreter(tree).interpret()
    # TODO: set another output stream


@pytest.mark.parametrize('stmt', ['var y = "y"; var x = "x"; x = y; print(x);'])
def test_ini_assign_var(stmt):
    tree = create_tree(stmt)
    interpreter = Interpreter(tree)
    interpreter.interpret()
    # local_vars = interpreter.local_vars
    # assert output = local_vars["x"]


