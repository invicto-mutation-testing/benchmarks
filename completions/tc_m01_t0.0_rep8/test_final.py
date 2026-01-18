

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
#         graph.add_vertex('A')  # Assuming we modify Graph to raise KeyError on duplicate

def test_get_vertex_nonexistent():
    graph = Graph()
    with pytest.raises(KeyError):
        graph.get_vertex('A')

def test_add_edge_normal():
    graph = Graph()
    graph.add_vertex('A')
    graph.add_vertex('B')
    graph.add_edge('A', 'B', 5)
    assert graph.does_edge_exist('A', 'B')
    assert graph.get_vertex('A').get_weight(graph.get_vertex('B')) == 5

def test_add_edge_nonexistent_vertex():
    graph = Graph()
    graph.add_vertex('A')
    with pytest.raises(KeyError):
        graph.add_edge('A', 'B', 5)

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
#         dijkstra(graph, Vertex('Z'))  # Assuming Vertex('Z') is not in graph

# def test_dijkstra_empty_graph():
#     graph = Graph()
#     with pytest.raises(ValueError):
#         dijkstra(graph, Vertex('A'))  # Assuming we modify dijkstra to raise ValueError on empty graph

def test_graph_contains_vertex():
    graph = Graph()
    graph.add_vertex('A')
    assert 'A' in graph  # This should pass in original and fail in mutant where 'in' is negated



def test_add_edge_default_weight():
    graph = Graph()
    graph.add_vertex('A')
    graph.add_vertex('B')
    graph.add_edge('A', 'B')
    assert graph.get_vertex('A').get_weight(graph.get_vertex('B')) == 1



def test_vertex_key_initialization():
    graph = Graph()
    graph.add_vertex('A')
    assert graph.get_vertex('A').get_key() == 'A'



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
    assert distances[graph.get_vertex('C')] == 3  # This should pass in original and fail in mutant where 'distance[neighbour] >= new_distance' allows incorrect updates

