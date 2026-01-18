

import pytest
from nds_script import Graph, Vertex, dijkstra


def test_add_vertex():
    graph = Graph()
    graph.add_vertex('A')
    assert 'A' in graph

def test_get_vertex():
    graph = Graph()
    graph.add_vertex('A')
    assert isinstance(graph.get_vertex('A'), Vertex)

# def test_add_vertex_duplicate_key():
#     graph = Graph()
#     graph.add_vertex('A')
#     with pytest.raises(KeyError):
#         graph.add_vertex('A')

def test_get_vertex_nonexistent_key():
    graph = Graph()
    with pytest.raises(KeyError):
        graph.get_vertex('A')

def test_add_edge():
    graph = Graph()
    graph.add_vertex('A')
    graph.add_vertex('B')
    graph.add_edge('A', 'B', 10)
    assert graph.does_edge_exist('A', 'B')

def test_add_edge_nonexistent_src():
    graph = Graph()
    graph.add_vertex('B')
    with pytest.raises(KeyError):
        graph.add_edge('A', 'B', 10)

def test_add_edge_nonexistent_dest():
    graph = Graph()
    graph.add_vertex('A')
    with pytest.raises(KeyError):
        graph.add_edge('A', 'B', 10)

def test_does_edge_exist():
    graph = Graph()
    graph.add_vertex('A')
    graph.add_vertex('B')
    graph.add_edge('A', 'B', 10)
    assert graph.does_edge_exist('A', 'B')

def test_does_edge_exist_nonexistent_edge():
    graph = Graph()
    graph.add_vertex('A')
    graph.add_vertex('B')
    assert not graph.does_edge_exist('A', 'B')

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

def test_dijkstra_edge_weight_mutation():
    graph = Graph()
    graph.add_vertex('A')
    graph.add_vertex('B')
    graph.add_edge('A', 'B', 1)  # Original code uses default weight=1, mutant uses weight=2
    source = graph.get_vertex('A')
    distances = dijkstra(graph, source)
    assert distances[graph.get_vertex('B')] == 1  # This should pass in original and fail in mutant



def test_vertex_key_initialization():
    graph = Graph()
    graph.add_vertex('A')
    vertex = graph.get_vertex('A')
    assert vertex.get_key() == 'A'

