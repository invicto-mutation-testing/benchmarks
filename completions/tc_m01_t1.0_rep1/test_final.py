

import pytest
from nds_script import Graph, Vertex, dijkstra


def test_empty_graph_init():
    graph = Graph()
    assert isinstance(graph, Graph)
    assert len(graph.vertices) == 0

def test_add_vertex():
    graph = Graph()
    graph.add_vertex("A")
    assert "A" in graph.vertices
    assert isinstance(graph.get_vertex("A"), Vertex)

def test_get_vertex_not_found():
    graph = Graph()
    graph.add_vertex("A")
    with pytest.raises(KeyError):
        graph.get_vertex("B")

def test_graph_contains_vertex():
    graph = Graph()
    graph.add_vertex("A")
    assert "A" in graph

def test_graph_does_not_contain_vertex():
    graph = Graph()
    assert "A" not in graph

def test_add_edge():
    graph = Graph()
    graph.add_vertex("A")
    graph.add_vertex("B")
    graph.add_edge("A", "B")
    assert graph.does_edge_exist("A", "B")

def test_add_edge_non_existent_source():
    graph = Graph()
    graph.add_vertex("B")
    with pytest.raises(KeyError):
        graph.add_edge("A", "B")

def test_add_edge_non_existent_destination():
    graph = Graph()
    graph.add_vertex("A")
    with pytest.raises(KeyError):
        graph.add_edge("A", "B")

def test_does_edge_exist():
    graph = Graph()
    graph.add_vertex("A")
    graph.add_vertex("B")
    graph.add_edge("A", "B")
    assert graph.does_edge_exist("A", "B")

def test_does_edge_not_exist():
    graph = Graph()
    graph.add_vertex("A")
    graph.add_vertex("B")
    assert not graph.does_edge_exist("A", "B")

def test_vertex_init():
    vertex = Vertex("A")
    assert vertex.key == "A"

def test_vertex_add_neighbour():
    vertex1 = Vertex("A")
    vertex2 = Vertex("B")
    vertex1.add_neighbour(vertex2, 10)
    assert vertex2 in vertex1.get_neighbours()
    assert vertex1.get_weight(vertex2) == 10

def test_vertex_does_it_point_to():
    vertex1 = Vertex("A")
    vertex2 = Vertex("B")
    vertex1.add_neighbour(vertex2, 10)
    assert vertex1.does_it_point_to(vertex2)

def test_vertex_does_not_point_to():
    vertex1 = Vertex("A")
    vertex2 = Vertex("B")
    assert not vertex1.does_it_point_to(vertex2)

def test_dijkstra_algorithm():
    graph = Graph()
    v1 = Vertex("A")
    v2 = Vertex("B")
    graph.vertices = {"A": v1, "B": v2}
    graph.add_edge("A", "B", 1)
    distances = dijkstra(graph, v1)
    assert distances[v1] == 0
    assert distances[v2] == 1

# def test_dijkstra_with_non_existent_source():
#     graph = Graph()
#     v1 = Vertex("A")
#     with pytest.raises(KeyError):
#         dijkstra(graph, v1)

def test_dijkstra_unconnected_vertices():
    graph = Graph()
    v1 = Vertex("A")
    v2 = Vertex("B")
    graph.vertices = {"A": v1, "B": v2}
    distances = dijkstra(graph, v1)
    assert distances[v1] == 0
    assert distances[v2] == float('inf')

def test_add_edge_default_weight():
    graph = Graph()
    graph.add_vertex("A")
    graph.add_vertex("B")
    graph.add_edge("A", "B")
    assert graph.get_vertex("A").get_weight(graph.get_vertex("B")) == 1



def test_dijkstra_inequality_fail_on_update():
    graph = Graph()
    graph.add_vertex("A")
    graph.add_vertex("B")
    graph.add_edge("A", "B", 1)
    graph.add_edge("B", "A", 1)  # Create a cycle to force re-evaluation on already visited nodes
    source_vertex = graph.get_vertex("A")
    distances = dijkstra(graph, source_vertex)
    assert distances[source_vertex] == 0  # This should pass as distance to self through cycles should not change
    assert distances[graph.get_vertex("B")] == 1  # This should pass for original but fail for mutated due to <= comparison

