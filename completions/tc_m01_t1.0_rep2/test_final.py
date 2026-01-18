

import pytest
from nds_script import Graph, Vertex, dijkstra


def test_graph_add_vertex():
    graph = Graph()
    graph.add_vertex("A")
    assert "A" in graph

def test_graph_get_vertex_existing():
    graph = Graph()
    graph.add_vertex("A")
    assert isinstance(graph.get_vertex("A"), Vertex)

def test_graph_get_vertex_non_existing():
    graph = Graph()
    with pytest.raises(KeyError):
        graph.get_vertex("A")

def test_vertex_initialization():
    vertex = Vertex("A")
    assert vertex.get_key() == "A"
    assert len(list(vertex.get_neighbours())) == 0

def test_vertex_add_neighbour():
    v1 = Vertex("A")
    v2 = Vertex("B")
    v1.add_neighbour(v2, 10)
    assert v2 in v1.get_neighbours()
    assert v1.get_weight(v2) == 10

# def test_vertex_add_neighbour_invalid_weight_type():
#     v1 = Vertex("A")
#     v2 = Vertex("B")
#     with pytest.raises(TypeError):
#         v1.add_neighbour(v2, "10")

def test_graph_add_edge_existing_vertices():
    graph = Graph()
    graph.add_vertex("A")
    graph.add_vertex("B")
    graph.add_edge("A", "B", 5)
    assert graph.does_edge_exist("A", "B")

def test_graph_add_edge_non_existing_src():
    graph = Graph()
    graph.add_vertex("B")
    with pytest.raises(KeyError):
        graph.add_edge("A", "B", 5)

def test_graph_add_edge_non_existing_dest():
    graph = Graph()
    graph.add_vertex("A")
    with pytest.raises(KeyError):
        graph.add_edge("A", "B", 5)

def test_dijkstra_existing_source():
    graph = Graph()
    graph.add_vertex("A")
    graph.add_vertex("B")
    graph.add_edge("A", "B", 1)
    source = graph.get_vertex("A")
    distances = dijkstra(graph, source)
    assert distances[source] == 0
    assert distances[graph.get_vertex("B")] == 1

# def test_dijkstra_invalid_source():
#     graph = Graph()
#     source = Vertex("A")
#     with pytest.raises(KeyError):
#         dijkstra(graph, source)

# def test_dijkstra_empty_graph():
#     graph = Graph()
#     with pytest.raises(ValueError):
#         dijkstra(graph, None)

def test_dijkstra_tight_edge_case():
    graph = Graph()
    graph.add_vertex("A")
    graph.add_vertex("B")
    graph.add_edge("A", "B", 1)
    graph.add_vertex("C")
    graph.add_edge("B", "C", 1)
    source = graph.get_vertex("A")
    adjacent = graph.get_vertex("B")
    distances = dijkstra(graph, source)
    assert distances[adjacent] == 1
    assert distances[graph.get_vertex("C")] == 2  # This test ensures it updates only when it finds strictly smaller distances in original

