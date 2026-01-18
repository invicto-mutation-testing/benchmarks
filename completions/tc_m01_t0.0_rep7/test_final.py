

import pytest
from nds_script import Graph, Vertex, dijkstra


def test_graph_initialization():
    graph = Graph()
    assert isinstance(graph, Graph)
    assert graph.vertices == {}

def test_vertex_initialization():
    vertex = Vertex("A")
    assert vertex.key == "A"
    assert vertex.points_to == {}

def test_add_vertex():
    graph = Graph()
    graph.add_vertex("A")
    assert "A" in graph.vertices
    assert isinstance(graph.get_vertex("A"), Vertex)

def test_add_edge():
    graph = Graph()
    graph.add_vertex("A")
    graph.add_vertex("B")
    graph.add_edge("A", "B", 5)
    assert graph.does_edge_exist("A", "B")
    assert graph.get_vertex("A").get_weight(graph.get_vertex("B")) == 5

def test_add_edge_nonexistent_vertex():
    graph = Graph()
    graph.add_vertex("A")
    with pytest.raises(KeyError):
        graph.add_edge("A", "B", 5)

def test_get_vertex_nonexistent():
    graph = Graph()
    with pytest.raises(KeyError):
        graph.get_vertex("A")

def test_dijkstra_basic():
    graph = Graph()
    graph.add_vertex("A")
    graph.add_vertex("B")
    graph.add_vertex("C")
    graph.add_edge("A", "B", 1)
    graph.add_edge("B", "C", 2)
    graph.add_edge("A", "C", 4)
    source = graph.get_vertex("A")
    distances = dijkstra(graph, source)
    assert distances[graph.get_vertex("A")] == 0
    assert distances[graph.get_vertex("B")] == 1
    assert distances[graph.get_vertex("C")] == 3

def test_dijkstra_unconnected():
    graph = Graph()
    graph.add_vertex("A")
    graph.add_vertex("B")
    source = graph.get_vertex("A")
    distances = dijkstra(graph, source)
    assert distances[graph.get_vertex("A")] == 0
    assert distances[graph.get_vertex("B")] == float('inf')

# def test_dijkstra_empty_graph():
#     graph = Graph()
#     with pytest.raises(ValueError):
#         dijkstra(graph, None)

# def test_dijkstra_nonexistent_source():
#     graph = Graph()
#     graph.add_vertex("A")
#     with pytest.raises(KeyError):
#         dijkstra(graph, Vertex("B"))

# def test_dijkstra_source_not_in_graph():
#     graph = Graph()
#     graph.add_vertex("A")
#     source = Vertex("B")
#     with pytest.raises(ValueError):
#         dijkstra(graph, source)

def test_graph_contains():
    graph = Graph()
    graph.add_vertex("A")
    assert "A" in graph
    assert "B" not in graph

def test_vertex_add_neighbour():
    graph = Graph()
    graph.add_vertex("A")
    graph.add_vertex("B")
    vertex_a = graph.get_vertex("A")
    vertex_b = graph.get_vertex("B")
    vertex_a.add_neighbour(vertex_b, 10)
    assert vertex_a.does_it_point_to(vertex_b)
    assert vertex_a.get_weight(vertex_b) == 10

def test_vertex_does_it_point_to_nonexistent():
    graph = Graph()
    graph.add_vertex("A")
    vertex_a = graph.get_vertex("A")
    vertex_b = Vertex("B")
    assert not vertex_a.does_it_point_to(vertex_b)

def test_vertex_get_weight_nonexistent():
    graph = Graph()
    graph.add_vertex("A")
    vertex_a = graph.get_vertex("A")
    vertex_b = Vertex("B")
    with pytest.raises(KeyError):
        vertex_a.get_weight(vertex_b)

def test_edge_default_weight():
    graph = Graph()
    graph.add_vertex("X")
    graph.add_vertex("Y")
    graph.add_edge("X", "Y")
    assert graph.get_vertex("X").get_weight(graph.get_vertex("Y")) == 1



def test_dijkstra_edge_case_update():
    graph = Graph()
    graph.add_vertex("A")
    graph.add_vertex("B")
    graph.add_vertex("C")
    graph.add_edge("A", "B", 1)
    graph.add_edge("B", "C", 2)
    graph.add_edge("A", "C", 3)
    source = graph.get_vertex("A")
    distances = dijkstra(graph, source)
    assert distances[graph.get_vertex("C")] == 3  # This should fail in mutant because it should be 3, not 2

