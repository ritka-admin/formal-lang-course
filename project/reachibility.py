import numpy as np
from scipy.sparse import dok_matrix
from pyformlang.finite_automaton import EpsilonNFA


def get_matrices(automaton: EpsilonNFA, states):
    n_states = len(states)
    res = dict()
    for v_from, label, v_to in automaton:
        mat = res.setdefault(label, dok_matrix((n_states, n_states), dtype=np.bool_))
        mat[states[v_from], states[v_to]] = True
    return res


def find_all_reachable(matrices: dict):
    res = None
    # get all reachable at the first step
    for matrix in matrices.values():
        if res is None:
            res = matrix
            continue
        res |= matrix
    if res is None:
        # Empty finite state machine that takes no input
        return set()

    # Transitive closure
    n_zeros = 0
    # While matrix is changing
    while res.count_nonzero() != n_zeros:
        n_zeros = res.count_nonzero()
        res += res @ res

    from_idx, to_idx = res.nonzero()
    return set(zip(from_idx, to_idx))


def find_reachable_for_each_vertex(automaton: EpsilonNFA) -> set:
    states = {k: i for i, k in enumerate(automaton.states)}
    matrices = get_matrices(automaton, states)
    v_reachable = find_all_reachable(matrices)
    rev_idx = {i: k for k, i in states.items()}
    result = set()
    for v_from, v_to in v_reachable:
        fro_id = rev_idx[v_from]
        to_id = rev_idx[v_to]
        if fro_id in automaton.start_states and to_id in automaton.final_states:
            result.add((fro_id.value, to_id.value))
    return result
