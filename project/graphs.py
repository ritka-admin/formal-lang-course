import networkx as nx
import cfpq_data as cd


def load_graph(graph_name: str):
    downloaded_g = cd.download(graph_name)
    graph = cd.graph_from_csv(downloaded_g)
    return graph


def save_graph(graph: nx.MultiDiGraph, path):
    nx.drawing.nx_pydot.write_dot(graph, path)


def count_vertices(graph: nx.MultiDiGraph):
    n_vertices = graph.number_of_nodes()
    return n_vertices


def count_edges(graph: nx.MultiDiGraph):
    m_edges = graph.number_of_edges()
    return m_edges


def get_labels(graph: nx.MultiDiGraph):
    labels = set()
    vertex_adj = list(graph.adjacency())
    for vertex in vertex_adj:
        for neighs in vertex:
            if type(neighs) is dict:
                for key in neighs.keys():
                    labels.add(neighs[key][0]['label'])
    return labels


def make_two_cycled_graph(fst_cycle_vertices, snd_cycle_vertices, labels: tuple):
    graph = cd.labeled_two_cycles_graph(fst_cycle_vertices, snd_cycle_vertices, labels=labels)
    return graph
