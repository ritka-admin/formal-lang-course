from typing import Union

import project.graphs
import networkx as nx
from pyformlang.regular_expression import Regex
from pyformlang.finite_automaton import (
    NondeterministicFiniteAutomaton,
    DeterministicFiniteAutomaton,
    EpsilonNFA,
    State
)


def regex_to_dfa(raw_regex: str) -> DeterministicFiniteAutomaton:
    regex = Regex(raw_regex)
    epsilon_nfa = regex.to_epsilon_nfa()
    deterministic = epsilon_nfa.to_deterministic()
    return deterministic.minimize()


def graph_to_nfa(graph: Union[str, nx.MultiDiGraph],
                 start_vs: set[int] = None,
                 final_vs: set[int] = None) -> EpsilonNFA:

    if type(graph) == str:
        graph = project.graphs.load_graph(graph_name=graph)

    nfa = EpsilonNFA.from_networkx(graph)

    if start_vs is None:
        for node in graph.nodes:
            nfa.add_start_state(node)
    else:
        for state in start_vs:
            nfa.add_start_state(state)

    if final_vs is None:
        for node in graph.nodes:
            nfa.add_final_state(node)
    else:
        for state in final_vs:
            nfa.add_final_state(state)

    return nfa
