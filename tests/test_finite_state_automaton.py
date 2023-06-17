from project.finite_state_automaton import *
from project.graphs import load_graph, make_two_cycled_graph, SourceType

from pyformlang.finite_automaton import NondeterministicFiniteAutomaton

graph = load_graph('skos', SourceType.DOWNLOAD)


def test_regex_to_dfa():
    dfa = regex_to_dfa("qwe | rty")
    res = NondeterministicFiniteAutomaton()
    res.add_start_state(0)
    res.add_final_state(1)
    res.add_transitions([(0, "qwe", 1), (0, "rty", 1)])
    res.to_deterministic()
    assert dfa == res


def test_nfa_start_final_states():
    nfa = graph_to_nfa(graph)
    nfa2 = graph_to_nfa(graph, start_vs={3, 4})
    res = graph.number_of_nodes()
    assert res == len(nfa.start_states)
    assert res == len(nfa.final_states)
    assert nfa2.start_states == {3, 4}


def test_graph_to_nfa():
    two_c_graph = make_two_cycled_graph(fst_cycle_vertices=[1, 2],
                                        snd_cycle_vertices=[3, 4],
                                        labels=("a", "a"))
    nfa = graph_to_nfa(two_c_graph, start_vs={0}, final_vs={0})
    regex = ('(a a a)*')
    dfa = regex_to_dfa(regex)
    assert dfa.is_equivalent_to(nfa)
