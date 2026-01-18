

import pytest
from nds_script import Graph, Vertex, dijkstra


def test_vertex_initialization():
    vertex = Vertex("A")
    assert vertex.key == "A"
    assert vertex.points_to == {}

def test_add_neighbour():
    v1 = Vertex("A")
    v2 = Vertex("B")
    v1.add_neighbour(v2, 10)
    assert v2 in v1.points_to
    assert v1.points_to[v2] == 10

def test_get_neighbours_empty():
    vertex = Vertex("A")
    assert list(vertex.get_neighbours()) == []

def test_get_neighbours_non_empty():
    v1 = Vertex("A")
    v2 = Vertex("B")
    v1.add_neighbour(v2, 10)
    assert list(v1.get_neighbours()) == [v2]

def test_does_it_point_to():
    v1 = Vertex("A")
    v2 = Vertex("B")
    v1.add_neighbour(v2, 5)
    assert v1.does_it_point_to(v2) == True

def test_does_it_point_to_false():
    v1 = Vertex("A")
    v2 = Vertex("B")
    v3 = Vertex("C")
    v1.add_neighbour(v2, 5)
    assert v1.does_it_point_to(v3) == False

def test_graph_initialization():
    graph = Graph()
    assert graph.vertices == {}

def test_add_vertex():
    graph = Graph()
    graph.add_vertex("A")
    assert "A" in graph.vertices
    assert isinstance(graph.vertices["A"], Vertex)

def test_get_vertex():
    graph = Graph()
    graph.add_vertex("A")
    assert graph.get_vertex("A") == graph.vertices["A"]

def test_get_vertex_exception():
    graph = Graph()
    with pytest.raises(KeyError):
        graph.get_vertex("A")

def test_contains_vertex():
    graph = Graph()
    graph.add_vertex("A")
    assert ("A" in graph) == True

def test_contains_vertex_false():
    graph = Graph()
    assert ("A" in graph) == False

def test_add_edge():
    graph = Graph()
    graph.add_vertex("A")
    graph.add_vertex("B")
    graph.add_edge("A", "B", 10)
    assert graph.does_edge_exist("A", "B") == True

def test_add_edge_non_existent_src():
    graph = Graph()
    graph.add_vertex("B")
    with pytest.raises(KeyError):
        graph.add_edge("A", "B", 10)

def test_add_edge_non_existent_dest():
    graph = Graph()
    graph.add_vertex("A")
    with pytest.raises(KeyError):
        graph.add_edge("A", "B", 10)

def test_does_edge_exist():
    graph = Graph()
    graph.add_vertex("A")
    graph.add_vertex("B")
    assert graph.does_edge_exist("A", "B") == False

def test_dijkstra_basic():
    graph = Graph()
    graph.add_vertex("A")
    graph.add_vertex("B")
    graph.add_vertex("C")
    graph.add_edge("A", "B", 1)
    graph.add_edge("B", "C", 2)
    graph.add_edge("A", "C", 4)
    distances = dijkstra(graph, graph.get_vertex("A"))
    assert distances[graph.get_vertex("A")] == 0
    assert distances[graph.get_vertex("B")] == 1
    assert distances[graph.get_vertex("C")] == 3

def test_dijkstra_no_edges():
    graph = Graph()
    graph.add_vertex("A")
    distances = dijkstra(graph, graph.get_vertex("A"))
    assert distances[graph.get_vertex("A")] == 0

# def test_dijkstra_invalid_source():
#     graph = Graph()
#     fake_vertex = Vertex("X")
#     with pytest.raises(ValueError):
#         dijkstra(graph, fake_vertex)

def test_edge_default_weight():
    graph = Graph()
    graph.add_vertex("A")
    graph.add_vertex("B")
    graph.add_edge("A", "B")
    assert graph.get_vertex("A").get_weight(graph.get_vertex("B")) == 1



def test_dijkstra_edge_case_update_comparison():
    graph = Graph()
    graph.add_vertex("A")
    graph.add_vertex("B")
    graph.add_vertex("C")
    graph.add_edge("A", "B", 2)
    graph.add_edge("B", "C", 2)
    graph.add_edge("A", "C", 1)
    distances = dijkstra(graph, graph.get_vertex("A"))
    assert distances[graph.get_vertex("C")] == 1  # This should fail with the mutant as the wrong comparison allows a direct path to override the intended shorter path.

