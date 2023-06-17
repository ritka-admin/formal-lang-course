import pytest
from antlr4 import *
from project.graphs import *
from project.finite_state_automaton import *
from project.interpreter import Interpreter
from pyformlang.finite_automaton import EpsilonNFA, State

from language.antlr_gen.LaLaLangParser import LaLaLangParser
from language.antlr_gen.LaLaLangLexer import LaLaLangLexer

two_c_graph: nx.MultiDiGraph = load_graph('graphs_dot/two_c', SourceType.FILE)
two_c_automaton: EpsilonNFA = graph_to_nfa(two_c_graph, two_c_graph.nodes, two_c_graph.nodes)

lol_graph: nx.MultiDiGraph = load_graph('graphs_dot/lol', SourceType.FILE)
lol_automaton: EpsilonNFA = graph_to_nfa(lol_graph, lol_graph.nodes, lol_graph.nodes)


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
    # TODO: assert output = local_vars["x"]


@pytest.mark.parametrize('stmt, expected',
                         [('var y = load("graphs_dot/two_c");', two_c_automaton),
                          ('var y = load("graphs_dot/lol");', lol_automaton)])
def test_load_func(stmt, expected):
    tree = create_tree(stmt)
    interpreter = Interpreter(tree)
    interpreter.interpret()
    assert interpreter._local_vars['y'].is_equivalent_to(expected)


@pytest.mark.parametrize('stmt, expected',
                         [('var y = load("graphs_dot/two_c"); var x = set_start({0}, y);'
                           "var k = set_final({1}, x);", two_c_automaton)])
def test_add_start_final_func(stmt, expected):
    two_c_automaton.remove_start_state(State(0))
    two_c_automaton.remove_final_state(State(1))
    tree = create_tree(stmt)
    interpreter = Interpreter(tree)
    interpreter.interpret()
    two_c_automaton.add_start_state(State(0))
    two_c_automaton.remove_final_state(State(1))
    assert interpreter._local_vars['k'].is_equivalent_to(expected)


@pytest.mark.parametrize('stmt', ['var x = {1, 2, 3}; print(x);'
                                  'var y = [1, "n", true]; print(y);'])
def test_collections(stmt):
    tree = create_tree(stmt)
    interpreter = Interpreter(tree)
    interpreter.interpret()
    # TODO: assert


@pytest.mark.parametrize('stmt', ['var x = {1, 2, "n"};'])
def test_typisation_incorrect(stmt):
    tree = create_tree(stmt)
    interpreter = Interpreter(tree)
    with pytest.raises(TypeError):
        interpreter.interpret()

# типизация: у сетов один и тот же тип; в функциях типа плюс умножить;
