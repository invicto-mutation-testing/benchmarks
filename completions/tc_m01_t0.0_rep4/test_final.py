

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

def test_add_edge():
    graph = Graph()
    graph.add_vertex('A')
    graph.add_vertex('B')
    graph.add_edge('A', 'B', 10)
    assert graph.does_edge_exist('A', 'B')

def test_add_edge_nonexistent_vertex():
    graph = Graph()
    graph.add_vertex('A')
    with pytest.raises(KeyError):
        graph.add_edge('A', 'B', 10)

def test_get_vertex_nonexistent():
    graph = Graph()
    with pytest.raises(KeyError):
        graph.get_vertex('A')

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
    assert distances[graph.get_vertex('C')] == 3

def test_dijkstra_unconnected():
    graph = Graph()
    graph.add_vertex('A')
    graph.add_vertex('B')
    source = graph.get_vertex('A')
    distances = dijkstra(graph, source)
    assert distances[graph.get_vertex('B')] == float('inf')

# def test_dijkstra_empty_graph():
#     graph = Graph()
#     with pytest.raises(ValueError):
#         dijkstra(graph, None)

# def test_dijkstra_nonexistent_source():
#     graph = Graph()
#     graph.add_vertex('A')
#     with pytest.raises(KeyError):
#         dijkstra(graph, Vertex('B'))

def test_vertex_initialization():
    vertex = Vertex('A')
    assert vertex.key == 'A'
    assert vertex.points_to == {}

def test_vertex_add_neighbour():
    vertex1 = Vertex('A')
    vertex2 = Vertex('B')
    vertex1.add_neighbour(vertex2, 5)
    assert vertex1.does_it_point_to(vertex2)
    assert vertex1.get_weight(vertex2) == 5

def test_vertex_get_neighbours():
    vertex1 = Vertex('A')
    vertex2 = Vertex('B')
    vertex1.add_neighbour(vertex2, 5)
    assert list(vertex1.get_neighbours()) == [vertex2]

def test_vertex_get_weight_nonexistent():
    vertex1 = Vertex('A')
    vertex2 = Vertex('B')
    with pytest.raises(KeyError):
        vertex1.get_weight(vertex2)

def test_vertex_does_it_point_to_nonexistent():
    vertex1 = Vertex('A')
    vertex2 = Vertex('B')
    assert not vertex1.does_it_point_to(vertex2)

def test_graph_contains():
    graph = Graph()
    graph.add_vertex('A')
    assert 'A' in graph



def test_dijkstra_edge_weight_mutation():
    graph = Graph()
    graph.add_vertex('A')
    graph.add_vertex('B')
    graph.add_edge('A', 'B')
    source = graph.get_vertex('A')
    distances = dijkstra(graph, source)
    assert distances[graph.get_vertex('B')] == 1  # This should pass in original and fail in mutant where default weight is 2



def test_dijkstra_edge_weight_equality():
    graph = Graph()
    graph.add_vertex('A')
    graph.add_vertex('B')
    graph.add_edge('A', 'B', 1)
    source = graph.get_vertex('A')
    distances = dijkstra(graph, source)
    assert distances[graph.get_vertex('B')] == 1

