from typing import Union, Set

import project.graphs
import networkx as nx
from project.reachibility import get_matrices
from scipy.sparse import dok_matrix, kron
from pyformlang.regular_expression import Regex
from pyformlang.finite_automaton import DeterministicFiniteAutomaton, EpsilonNFA, Epsilon


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
        graph = project.graphs.load_graph(graph, project.graphs.SourceType.DOWNLOAD)

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


def automatons_union(automaton1: EpsilonNFA, automaton2: EpsilonNFA):
    res = EpsilonNFA()

    for v_from, label, v_to in automaton1:
        res.add_transition(v_from, label, v_to)

    for v_from, label, v_to in automaton2:
        res.add_transition(v_from, label, v_to)

    for start in automaton1.start_states:
        res.add_start_state(start)

    for start in automaton2.start_states:
        res.add_start_state(start)

    for final in automaton1.final_states:
        res.add_final_state(final)

    for final in automaton2.final_states:
        res.add_final_state(final)

    return res


def automaton_concat(automaton1: EpsilonNFA, automaton2: EpsilonNFA):
    res = EpsilonNFA()

    for v_from, label, v_to in automaton1:
        res.add_transition(v_from, label, v_to)

    for v_from, label, v_to in automaton2:
        res.add_transition(v_from, label, v_to)

    for start in automaton1.start_states:
        res.add_start_state(start.value)

    for final in automaton1.final_states:
        for start in automaton2.start_states:
            res.add_transition(final, Epsilon(), start)

    for final in automaton2.final_states:
        res.add_final_state(final)

    return res


def automaton_intersect(automaton1: EpsilonNFA, automaton2: EpsilonNFA):
    states1 = {k: i for i, k in enumerate(automaton1.states)}
    states2 = {k: i for i, k in enumerate(automaton2.states)}
    matrix1 = get_matrices(automaton1, states1)
    matrix2 = get_matrices(automaton2, states2)
    common_letters = set(matrix1.keys()).intersection(matrix2.keys())
    common_matrices = {m: kron(matrix1[m], matrix2[m]) for m in common_letters}

    res = EpsilonNFA()

    for letter, mat in common_matrices.items():
        from_idx, to_idx = mat.nonzero()
        for v_from, v_ in zip(from_idx, to_idx):
            res.add_transition(v_from, letter, v_)

    for start1 in automaton1.start_states:
        for start2 in automaton2.start_states:
            res.add_start_state(states1[start1] * len(states2) + states2[start2])

    for final1 in automaton1.final_states:
        for final2 in automaton2.final_states:
            res.add_final_state(states1[final1] * len(states2) + states2[final2])

    return res


def automaton_kleene(automaton: EpsilonNFA):
    res = automaton.copy()

    for final in automaton.final_states:
        for start in automaton.start_states:
            res.add_transition(final, Epsilon(), start)

    return res
