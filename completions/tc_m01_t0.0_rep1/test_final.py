

import pytest
from nds_script import Graph, Vertex, dijkstra


def test_graph_initialization():
    graph = Graph()
    assert isinstance(graph, Graph)
    assert graph.vertices == {}

def test_add_vertex():
    graph = Graph()
    graph.add_vertex('A')
    assert 'A' in graph.vertices
    assert isinstance(graph.get_vertex('A'), Vertex)

# def test_add_vertex_duplicate_key():
#     graph = Graph()
#     graph.add_vertex('A')
#     with pytest.raises(KeyError):
#         graph.add_vertex('A')

def test_get_vertex_nonexistent():
    graph = Graph()
    with pytest.raises(KeyError):
        graph.get_vertex('A')

def test_add_edge():
    graph = Graph()
    graph.add_vertex('A')
    graph.add_vertex('B')
    graph.add_edge('A', 'B', 5)
    assert graph.does_edge_exist('A', 'B')

def test_add_edge_nonexistent_vertex():
    graph = Graph()
    graph.add_vertex('A')
    with pytest.raises(KeyError):
        graph.add_edge('A', 'C', 5)

def test_does_edge_exist_nonexistent():
    graph = Graph()
    graph.add_vertex('A')
    graph.add_vertex('B')
    assert not graph.does_edge_exist('A', 'B')

def test_vertex_initialization():
    vertex = Vertex('A')
    assert vertex.key == 'A'
    assert vertex.points_to == {}

def test_add_neighbour():
    vertex1 = Vertex('A')
    vertex2 = Vertex('B')
    vertex1.add_neighbour(vertex2, 10)
    assert vertex1.does_it_point_to(vertex2)
    assert vertex1.get_weight(vertex2) == 10

def test_get_neighbours_empty():
    vertex = Vertex('A')
    assert list(vertex.get_neighbours()) == []

def test_get_weight_nonexistent():
    vertex1 = Vertex('A')
    vertex2 = Vertex('B')
    with pytest.raises(KeyError):
        vertex1.get_weight(vertex2)

def test_dijkstra_basic():
    graph = Graph()
    graph.add_vertex('A')
    graph.add_vertex('B')
    graph.add_vertex('C')
    graph.add_edge('A', 'B', 1)
    graph.add_edge('B', 'C', 2)
    graph.add_edge('A', 'C', 4)
    source = graph.get_vertex('A')
    distances = dijkstra(graph, source)
    assert distances[graph.get_vertex('A')] == 0
    assert distances[graph.get_vertex('B')] == 1
    assert distances[graph.get_vertex('C')] == 3

def test_dijkstra_unconnected():
    graph = Graph()
    graph.add_vertex('A')
    graph.add_vertex('B')
    source = graph.get_vertex('A')
    distances = dijkstra(graph, source)
    assert distances[graph.get_vertex('A')] == 0
    assert distances[graph.get_vertex('B')] == float('inf')

# def test_dijkstra_nonexistent_source():
#     graph = Graph()
#     graph.add_vertex('A')
#     with pytest.raises(KeyError):
#         dijkstra(graph, Vertex('Z'))

def test_graph_contains_vertex():
    graph = Graph()
    graph.add_vertex('A')
    assert 'A' in graph  # This should pass in original and fail in mutant due to the negation in __contains__ method



def test_add_edge_default_weight():
    graph = Graph()
    graph.add_vertex('A')
    graph.add_vertex('B')
    graph.add_edge('A', 'B')
    assert graph.get_vertex('A').get_weight(graph.get_vertex('B')) == 1



def test_dijkstra_edge_case_update():
    graph = Graph()
    graph.add_vertex('A')
    graph.add_vertex('B')
    graph.add_vertex('C')
    graph.add_edge('A', 'B', 1)
    graph.add_edge('B', 'C', 2)
    graph.add_edge('A', 'C', 3)
    source = graph.get_vertex('A')
    distances = dijkstra(graph, source)
    assert distances[graph.get_vertex('C')] == 3  # Should be 3 in original, fails in mutant where it would be 2

