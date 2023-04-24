from typing import Dict

import networkx as nx
from scipy import sparse
from pyformlang.cfg import CFG, Variable, Terminal
from project.cf_grammar import cfg_to_weak_normal_from


def matrix(graph: nx.MultiDiGraph, cfg: CFG):
    wcnf = cfg_to_weak_normal_from(cfg)
    matrix = dict()
    for var in wcnf.variables:
        matrix[var] = sparse.dok_matrix((graph.number_of_nodes(),
                                        graph.number_of_nodes()),
                                        dtype=bool)

    epsilon_productions = {p.head.value for p in wcnf.productions if not p.body}
    term_productions = {p for p in wcnf.productions if len(p.body) == 1}
    nonterminal_productions = {p for p in wcnf.productions if len(p.body) == 2}

    for u, v, t in graph.edges(data=True):
        for p in term_productions:
            if t["label"] == p.body[0].value:
                matrix[p.head.value][u, v] = True

    for i in range(graph.number_of_nodes()):
        for p in epsilon_productions:
            matrix[p][i, i] = True

    changed = True
    while changed:
        changed = False
        for p in nonterminal_productions:
            n_zeros = matrix[p.head.value].nnz
            matrix[p.head.value] += matrix[p.body[0].value] @ matrix[p.body[1].value]
            new_zeros = matrix[p.head.value].nnz
            changed = False if n_zeros == new_zeros else True

    return {
        (u, nonterm.value, v)
        for nonterm, m in matrix.items()
        for u, v in zip(*m.nonzero())  # pass two args to the zip function (row and column arrays)
    }


def graph_query_matrix(graph: nx.MultiDiGraph, cfg: CFG, start_vertices,
                         final_vertices, start_nonterminal: Variable) -> Dict[int, int]:
    matrix_res = matrix(graph, cfg)
    ans = {v: set() for v in start_vertices}
    for u, nonterm, v in matrix_res:
        if u in start_vertices and v in final_vertices and start_nonterminal == nonterm:
            ans[u].add(v)
    return ans


def cfg_from_text_matrix(graph: nx.MultiDiGraph, cfg: str):
    return matrix(graph, CFG.from_text(cfg))


def cfg_from_file_matrix(graph: nx.MultiDiGraph, file: str):
    with open(file) as f:
        return cfg_from_text_matrix(graph, f.read())
