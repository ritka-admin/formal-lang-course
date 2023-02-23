import os
import pytest
import project.graphs  # on import will print something from __init__ file


graph1 = project.graphs.load_graph('skos')
graph2 = project.graphs.load_graph('wc')


def test_vertices():
    ans1 = project.graphs.count_vertices(graph1)
    ans2 = project.graphs.count_vertices(graph2)
    assert graph1.number_of_nodes() == ans1
    assert graph2.number_of_nodes() == ans2


def test_edges():
    ans1 = project.graphs.count_edges(graph1)
    ans2 = project.graphs.count_edges(graph2)
    assert graph1.number_of_edges() == ans1
    assert graph2.number_of_edges() == ans2


def test_labels():
    ans = project.graphs.get_labels(graph2)
    assert {'a', 'd'} == ans


def test_two_cycled():
    graph = project.graphs.make_two_cycled_graph(42, 21, ("a", "b"))
    print(list(graph.adjacency()))
    assert graph.number_of_nodes() == 42 + 21 + 1
    assert project.graphs.get_labels(graph) == {"a", "b"}


def test_save_graph():
    project.graphs.save_graph(graph2, 'lol')
    assert 'lol' in os.listdir('.')
    os.remove('lol')
