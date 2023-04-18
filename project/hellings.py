import networkx as nx
from typing import Set, Tuple, Dict
from pyformlang.cfg import CFG, Variable
from pyformlang.cfg.terminal import Terminal
from project.cf_grammar import cfg_to_weak_normal_from


def hellings(graph: nx.MultiDiGraph, cfg: CFG) -> Set[Tuple]:
    """
    Apply hellings algorithm for finding paths

    Parameters:
        graph: graph to search through
        cfg: context-free grammar

    Returns:
        Set of tuples of vertex1, nonterminal, vertex2, where vertex1, vertex2
        are the vertices that are adjacent to the same edge, and nonterminal
        is a label on that edge
    """
    wcnf = cfg_to_weak_normal_from(cfg)

    epsilon_production_head = {p.head.value for p in wcnf.productions if not p.body}
    terminal_production_head = {p for p in wcnf.productions if len(p.body) == 1}
    nonterminals_production_head = {p for p in wcnf.productions if len(p.body) == 2}

    epsilon_edges = set()
    # add epsilon edge to each vertex
    for h in epsilon_production_head:
        for v in range(graph.number_of_nodes()):
            epsilon_edges.add((v, h, v))

    terminal_edges = set()
    # add graph edges that has the 'p.body[0]' terminal label on it
    for e1, e2, edge_info in graph.edges(data=True):
        for p in terminal_production_head:
            if p.body[0] == Terminal(edge_info["label"]):
                terminal_edges.add((e1, p.head.value, e2))

    rules = epsilon_edges.union(terminal_edges)

    rules_copy = rules.copy()
    # add new edges that are created via several rules
    while rules_copy:
        u, A, v = rules_copy.pop()
        step = set()

        for x, B, y in rules:
            if y == u:
                new_edges = set()
                for p in nonterminals_production_head:
                    if p.body[0].value == B and p.body[1].value == A \
                            and (x, p.head.value, v) not in rules:
                        new_edges.add((x, p.head.value, v))
                step |= new_edges

        rules |= step
        rules_copy |= step
        step.clear()

        for x, B, y in rules:
            if x == v:
                new_edges = set()
                for p in nonterminals_production_head:
                    if p.body[0].value == A and p.body[1].value == B \
                            and (u, p.head.value, y) not in rules:
                        new_edges.add((u, p.head.value, y))
                step |= new_edges

        rules |= step
        rules_copy |= step

    return rules


def graph_query(graph: nx.MultiDiGraph, cfg: CFG, start_vertices,
                final_vertices, start_nonterminal: Variable) -> Dict[int, int]:
    """
    Queries the graph using hellings algorithm

    Parameters:
        graph: graph to query
        cfg: context-free grammar
        start_vertices: collection of start vertices
        final_vertices: collection of final vertices
        start_nonterminal: nonterminal to start the search from

    Returns:
        the dictionary of starting nodes to the reachable vertices
    """
    ans = {u: set() for u in start_vertices}
    hellings_res = hellings(graph, cfg)
    for u, non, v in hellings_res:
        if non == start_nonterminal and u in start_vertices \
                and v in final_vertices:
            ans[u].add(v)
    return ans


def from_text_hellings(graph: nx.MultiDiGraph, cfg: str) -> Set[Tuple]:
    """
    Run hellings algorithm with the cfg from the text
    """
    return hellings(graph, CFG.from_text(cfg))


def from_file_hellings(graph: nx.MultiDiGraph, file: str) -> Set[Tuple]:
    """
    Run hellings algorithm with the cfg from the provided file
    """
    with open(file) as file:
        return from_text_hellings(graph, file.read())
