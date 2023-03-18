from typing import Union, Set

import project.graphs
import networkx as nx
from pyformlang.regular_expression import Regex
from pyformlang.finite_automaton import DeterministicFiniteAutomaton, EpsilonNFA


def regex_to_dfa(raw_regex: str) -> DeterministicFiniteAutomaton:
    """
    Turns regular expression into deterministic finite automaton.

    Parameters:
         raw_regex: regular expression as a string

    Returns:
        minimized deterministic finite automaton
        built upon the provided regular expression
    """
    regex = Regex(raw_regex)
    epsilon_nfa = regex.to_epsilon_nfa()
    return epsilon_nfa.minimize()


def graph_to_nfa(graph: Union[str, nx.MultiDiGraph],
                 start_vs: Set[int] = None,
                 final_vs: Set[int] = None) -> EpsilonNFA:
    """
    Builds a nondeterministic finite automaton for the provided graph.

    Parameters:
        graph: graph name or networkx graph itself
        start_vs: vertices that will be marked as starting states
        final_vs: vertices that will be marked as final states

    Returns:
        Nondeterministic finite automaton. If start_vs or final_vs equals to None,
        returns a graph with all vertices marked as start / final states.
    """
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
