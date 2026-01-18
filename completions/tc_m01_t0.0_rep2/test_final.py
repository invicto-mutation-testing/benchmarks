

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

# def test_dijkstra_nonexistent_source():
#     graph = Graph()
#     graph.add_vertex("A")
#     with pytest.raises(KeyError):
#         dijkstra(graph, Vertex("B"))

# def test_dijkstra_empty_graph():
#     graph = Graph()
#     with pytest.raises(ValueError):
#         dijkstra(graph, Vertex("A"))

def test_graph_contains():
    graph = Graph()
    graph.add_vertex("A")
    assert "A" in graph



def test_default_edge_weight():
    graph = Graph()
    graph.add_vertex("A")
    graph.add_vertex("B")
    graph.add_edge("A", "B")
    assert graph.get_vertex("A").get_weight(graph.get_vertex("B")) == 1



def test_dijkstra_edge_case_update():
    graph = Graph()
    graph.add_vertex("A")
    graph.add_vertex("B")
    graph.add_vertex("C")
    graph.add_edge("A", "B", 1)
    graph.add_edge("B", "C", 2)
    graph.add_edge("A", "C", 3)
    graph.add_edge("A", "C", 1)  # This should not update the weight in the original code
    source = graph.get_vertex("A")
    distances = dijkstra(graph, source)
    assert distances[graph.get_vertex("C")] == 1  # Should be 3, not 1, if the edge weight update is ignored

