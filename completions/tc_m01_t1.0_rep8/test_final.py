

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

def test_get_vertex_not_added():
    graph = Graph()
    with pytest.raises(KeyError):
        graph.get_vertex('A')

def test_vertex_in_graph():
    graph = Graph()
    graph.add_vertex('A')
    assert 'A' in graph

def test_add_edge_normal_case():
    graph = Graph()
    graph.add_vertex('A')
    graph.add_vertex('B')
    graph.add_edge('A', 'B')
    assert graph.does_edge_exist('A', 'B')

def test_add_edge_nonexistent_source_vertex():
    graph = Graph()
    graph.add_vertex('B')
    with pytest.raises(KeyError):
        graph.add_edge('A', 'B')

def test_add_edge_nonexistent_destination_vertex():
    graph = Graph()
    graph.add_vertex('A')
    with pytest.raises(KeyError):
        graph.add_edge('A', 'B')

def test_add_edge_self_loop():
    graph = Graph()
    graph.add_vertex('A')
    graph.add_edge('A', 'A')
    assert graph.does_edge_exist('A', 'A')

def test_does_edge_exist_false():
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
    assert vertex1.get_weight(vertex2) == 10

def test_get_neighbours_empty():
    vertex = Vertex('A')
    assert list(vertex.get_neighbours()) == []

# def test_get_neighbours():
#     vertex1 = Vertex('A')
#     vertex2 = Vertex('B')
#     vertex1.add_neighbour(vertex2, 10)
#     assert list(vertex.get_neighbours()) == [vertex2]

def test_does_it_point_to_false():
    vertex1 = Vertex('A')
    vertex2 = Vertex('B')
    assert not vertex1.does_it_point_to(vertex2)

def test_dijkstra_no_vertices():
    graph = Graph()
    with pytest.raises(KeyError):
        dijkstra(graph, graph.get_vertex('A'))

def test_dijkstra_one_vertex():
    graph = Graph()
    graph.add_vertex('A')
    source = graph.get_vertex('A')
    distances = dijkstra(graph, source)
    assert distances == {source: 0}

def test_dijkstra_source_to_two_other_vertices():
    graph = Graph()
    graph.add_vertex('A')
    graph.add_vertex('B')
    graph.add_vertex('C')
    graph.add_edge('A', 'B', 5)
    graph.add_edge('A', 'C', 10)
    source = graph.get_vertex('A')
    distances = dijkstra(graph, source)
    assert distances == {
        graph.get_vertex('A'): 0,
        graph.get_vertex('B'): 5,
        graph.get_vertex('C'): 10
    }

def test_dijkstra_unconnected_vertex():
    graph = Graph()
    graph.add_vertex('A')
    graph.add_vertex('B')
    graph.add_vertex('C')
    graph.add_edge('A', 'B', 5)
    source = graph.get_vertex('A')
    distances = dijkstra(graph, source)
    assert distances[graph.get_vertex('C')] == float('inf')

def test_dijkstra_incorrect_default_weight():
    graph = Graph()
    graph.add_vertex('A')
    graph.add_vertex('B')
    graph.add_edge('A', 'B')  # Uses default weight, should be 1 in original, 2 in mutant
    source = graph.get_vertex('A')
    distances = dijkstra(graph, source)
    assert distances[graph.get_vertex('B')] == 1  # This assertion will pass in original and fail in mutant



def test_dijkstra_edge_relaxation_minimal_case():
    graph = Graph()
    graph.add_vertex('A')
    graph.add_vertex('B')
    graph.add_edge('A', 'B', 2)
    source = graph.get_vertex('A')
    distances = dijkstra(graph, source)
    assert distances[graph.get_vertex('B')] == 2

