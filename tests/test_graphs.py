import os
from project.graphs import *
import networkx as nx


graph1 = load_graph('skos', SourceType.DOWNLOAD)
graph2 = load_graph('wc', SourceType.DOWNLOAD)


def test_vertices():
    ans1 = count_vertices(graph1)
    ans2 = count_vertices(graph2)
    assert graph1.number_of_nodes() == ans1
    assert graph2.number_of_nodes() == ans2


def test_edges():
    ans1 = count_edges(graph1)
    ans2 = count_edges(graph2)
    assert graph1.number_of_edges() == ans1
    assert graph2.number_of_edges() == ans2


def test_labels():
    ans = get_labels(graph2)
    assert {'a', 'd'} == ans


def test_save_graph():
    save_graph(graph2, 'lol')
    new_graph = nx.drawing.nx_pydot.read_dot('graphs_dot/lol')
    # read_dot adds \n as a new vertex to adjacency list
    new_graph.remove_node('\\n')
    assert get_graph_info(new_graph) == get_graph_info(graph2)
    os.remove('lol')


def test_two_cycled():
    graph = make_and_save_two_cycled_graph(42, 21, ("a", "b"), path='two_c')
    new_graph = nx.drawing.nx_pydot.read_dot('two_c')
    new_graph.remove_node('\\n')
    assert get_graph_info(new_graph) == get_graph_info(graph)
    os.remove('two_c')
