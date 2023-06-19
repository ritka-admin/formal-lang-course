import sys
from io import StringIO

import pytest
from antlr4 import *
from project.types import *
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


class Capturing(list):
    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._stringio = StringIO()
        return self

    def __exit__(self, *args):
        self.extend(self._stringio.getvalue().splitlines())
        sys.stdout = self._stdout


@pytest.mark.parametrize('stmt, expected', [('var x = false; print(x);', False),
                                            ('print(5);', 5), ('print("string");', "string")])
def test_print_stmt(stmt, expected):
    tree = create_tree(stmt)
    sys.stdout = StringIO()
    with Capturing() as output:
        Interpreter(tree).interpret()
    assert output[0] == str(expected)


@pytest.mark.parametrize('stmt', ['var y = "y"; var x = "x"; x = y; print(x);'])
def test_ini_assign_var(stmt):
    tree = create_tree(stmt)
    interpreter = Interpreter(tree)
    with Capturing() as output:
        interpreter.interpret()
    assert output[0] == interpreter._global_vars["x"].value


@pytest.mark.parametrize('stmt, expected', [('var x = {1, 2, 3}; print(x);', {1, 2, 3}),
                                            ('var y = [1, "n", true]; print(y);', [1, "n", True])])
def test_collections(stmt, expected):
    tree = create_tree(stmt)
    interpreter = Interpreter(tree)
    interpreter.interpret()
    with Capturing() as output:
        interpreter.interpret()
    assert output[0] == str(expected)


@pytest.mark.parametrize('stmt, expected',
                         [('var y = load("graphs_dot/two_c");', two_c_automaton),
                          ('var y = load("graphs_dot/lol");', lol_automaton)])
def test_load_func(stmt, expected):
    tree = create_tree(stmt)
    interpreter = Interpreter(tree)
    interpreter.interpret()
    assert interpreter._global_vars['y'].value.is_equivalent_to(expected)


@pytest.mark.parametrize('stmt, expected',
                         [('var y = load("graphs_dot/two_c"); var x = add_start({0}, y);'
                           "var k = add_final({1}, x);", two_c_automaton)])
def test_add_start_final_func(stmt, expected):
    two_c_automaton.remove_start_state(State('0'))
    two_c_automaton.remove_final_state(State('1'))
    tree = create_tree(stmt)
    interpreter = Interpreter(tree)
    interpreter.interpret()
    two_c_automaton.add_start_state(State('0'))
    two_c_automaton.add_final_state(State('1'))
    assert interpreter._global_vars['k'].value.is_equivalent_to(expected)


@pytest.mark.parametrize('stmt, expected',
                         [(
                                 'var y = load("graphs_dot/two_c"); '
                                 'var x = get_start(y); '
                                 'var o = get_final(y);',
                                 (two_c_automaton.start_states, two_c_automaton.final_states))])
def test_get_start_final(stmt, expected):
    tree = create_tree(stmt)
    interpreter = Interpreter(tree)
    interpreter.interpret()
    assert interpreter._global_vars['x'].value == expected[0]
    assert interpreter._global_vars['o'].value == expected[1]


@pytest.mark.parametrize('stmt, expected',
                         [(
                            'var y = load("graphs_dot/two_c"); '
                            'var x = get_vertices(y);',
                            set(two_c_graph.nodes)
                         ),
                          (
                            'var y = load("graphs_dot/lol"); '
                            'var x = get_edges(y);',
                            set((x, y, z) for (x, y, z) in lol_automaton)
                         ),
                          (
                             'var y = load("graphs_dot/lol"); '
                             'var x = get_labels(y)',
                             get_graph_info(lol_graph).labels
                         )
                         ])
def test_get_vert_edges_labels(stmt, expected):
    tree = create_tree(stmt)
    interpreter = Interpreter(tree)
    interpreter.interpret()
    assert interpreter._global_vars['x'].value == expected


@pytest.mark.parametrize('stmt', ['var x = {1, 2, "n"};'])
def test_typisation_incorrect(stmt):
    tree = create_tree(stmt)
    interpreter = Interpreter(tree)
    with pytest.raises(TypeError):
        interpreter.interpret()


@pytest.mark.parametrize('stmt', ['var y = \[g] -> g;',
                                  'var y = \[g] -> load(g);'])
def test_lambda_funcs(stmt):
    tree = create_tree(stmt)
    interpreter = Interpreter(tree)
    interpreter.interpret()
    assert isinstance(interpreter._global_vars['y'], LaLaLambda)
    assert interpreter._global_vars['y'].args == ['g']


@pytest.mark.parametrize('stmt', ['var l = load("graphs_dot/lol"); var m = load("graphs_dot/two_c");'
                                  'var x = [l, m];'
                                  'var y = map(\[g] -> add_final({0}, g), x);'])
def test_map(stmt):
    tree = create_tree(stmt)
    interpreter = Interpreter(tree)
    interpreter.interpret()
    assert '0' in interpreter._global_vars['y'][0].value.final_states
    assert '0' in interpreter._global_vars['y'][1].value.final_states

# типизация: у сетов один и тот же тип; в функциях типа плюс умножить;
