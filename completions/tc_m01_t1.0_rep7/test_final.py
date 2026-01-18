

import pytest
from nds_script import Graph, Vertex, dijkstra


def test_add_vertex():
    graph = Graph()
    graph.add_vertex('A')
    assert 'A' in graph.vertices

def test_add_vertex_existing():
    graph = Graph()
    graph.add_vertex('A')
    graph.add_vertex('A')  # Re-adding should not throw an error, just silently solves
    assert 'A' in graph.vertices and len(graph.vertices) == 1

def test_get_existing_vertex():
    graph = Graph()
    graph.add_vertex('A')
    v = graph.get_vertex('A')
    assert isinstance(v, Vertex) and v.key == 'A'

def test_get_nonexistent_vertex():
    graph = Graph()
    with pytest.raises(KeyError):
        graph.get_vertex('B')

def test_contains_vertex():
    graph = Graph()
    graph.add_vertex('A')
    assert 'A' in graph

def test_contains_nonexistent_vertex():
    graph = Graph()
    assert 'B' not in graph

def test_add_edge_normal():
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

def test_does_edge_exist_true():
    graph = Graph()
    graph.add_vertex('A')
    graph.add_vertex('B')
    graph.add_edge('A', 'B', 1)
    assert graph.does_edge_exist('A', 'B')

def test_does_edge_exist_false():
    graph = Graph()
    graph.add_vertex('A')
    graph.add_vertex('B')
    assert not graph.does_edge_exist('A', 'B')

def test_add_neighbour():
    graph = Graph()
    graph.add_vertex('A')
    graph.add_vertex('B')
    vertex_a = graph.get_vertex('A')
    vertex_b = graph.get_vertex('B')
    vertex_a.add_neighbour(vertex_b, 5)
    assert vertex_b in vertex_a.get_neighbours()

def test_vertex_points_to():
    graph = Graph()
    graph.add_vertex('A')
    graph.add_vertex('B')
    vertex_a = graph.get_vertex('A')
    vertex_b = graph.get_vertex('B')
    vertex_a.add_neighbour(vertex_b, 5)
    assert vertex_a.does_it_point_to(vertex_b)

def test_dijkstra_simple():
    graph = Graph()
    graph.add_vertex('A')
    graph.add_vertex('B')
    graph.add_vertex('C')
    graph.add_edge('A', 'B', 1)
    graph.add_edge('B', 'C', 1)
    graph.add_edge('A', 'C', 3)
    distances = dijkstra(graph, graph.get_vertex('A'))
    assert distances[graph.get_vertex('C')] == 2

def test_dijkstra_unreachable():
    graph = Graph()
    graph.add_vertex('A')
    graph.add_vertex('B')
    graph.add_edge('A', 'B', 1)
    distances = dijkstra(graph, graph.get_vertex('A'))
    assert distances[graph.get_vertex('B')] == 1

def test_dijkstra_distance_to_self():
    graph = Graph()
    graph.add_vertex('A')
    distances = dijkstra(graph, graph.get_vertex('A'))
    assert distances[graph.get_vertex('A')] == 0

def test_add_edge_default_weight():
    graph = Graph()
    graph.add_vertex('X')
    graph.add_vertex('Y')
    graph.add_edge('X', 'Y')
    assert graph.does_edge_exist('X', 'Y') and graph.get_vertex('X').get_weight(graph.get_vertex('Y')) == 1



def test_dijkstra_equal_distances():
    graph = Graph()
    graph.add_vertex('A')
    graph.add_vertex('B')
    graph.add_edge('A', 'B', 1)
    graph.add_edge('A', 'B', 1)  # Adding the same edge with the same weight
    distances = dijkstra(graph, graph.get_vertex('A'))
    # Should maintain the shortest distance as 1 for both original and mutant, but mutant could have bugs in handling this.
    assert distances[graph.get_vertex('B')] == 1

