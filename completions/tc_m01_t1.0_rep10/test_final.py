

import pytest
from nds_script import Graph, Vertex, dijkstra


def test_graph_initial_empty_vertices():
    graph = Graph()
    assert isinstance(graph.vertices, dict) and len(graph.vertices) == 0

def test_add_vertex_new_key():
    graph = Graph()
    graph.add_vertex("A")
    assert "A" in graph.vertices

def test_get_vertex_existing_key():
    graph = Graph()
    graph.add_vertex("A")
    vertex = graph.get_vertex("A")
    assert isinstance(vertex, Vertex) and vertex.key == "A"

def test_get_vertex_non_existing_key():
    graph = Graph()
    with pytest.raises(KeyError):
        graph.get_vertex("A")

def test_add_edge_valid_keys():
    graph = Graph()
    graph.add_vertex("A")
    graph.add_vertex("B")
    graph.add_edge("A", "B")
    assert graph.does_edge_exist("A", "B")

def test_add_edge_invalid_src_key():
    graph = Graph()
    graph.add_vertex("B")
    with pytest.raises(KeyError):
        graph.add_edge("A", "B")

def test_add_edge_invalid_dest_key():
    graph = Graph()
    graph.add_vertex("A")
    with pytest.raises(KeyError):
        graph.add_edge("A", "B")

def test_dijkstra_source_in_graph():
    graph = Graph()
    graph.add_vertex("A")
    graph.add_edge("A", "A")
    source = graph.get_vertex("A")
    distances = dijkstra(graph, source)
    assert distances[source] == 0

# def test_dijkstra_source_not_in_graph():
#     graph = Graph()
#     graph.add_vertex("A")
#     source = Vertex("B")
#     with pytest.raises(ValueError):
#         dijkstra(graph, source)

# def test_dijkstra_empty_graph():
#     graph = Graph()
#     with pytest.raises(ValueError):
#         dijkstra(graph, None)

def test_dijkstra_graph_with_no_edges():
    graph = Graph()
    graph.add_vertex("A")
    source = graph.get_vertex("A")
    distances = dijkstra(graph, source)
    assert distances[source] == 0 and all(dist == float('inf') for v, dist in distances.items() if v != source)

def test_vertex_initial_empty_points_to():
    vertex = Vertex("A")
    assert isinstance(vertex.points_to, dict) and len(vertex.points_to) == 0

def test_add_neighbour_new():
    vertex = Vertex("A")
    neighbour = Vertex("B")
    vertex.add_neighbour(neighbour, 5)
    assert vertex.does_it_point_to(neighbour)

def test_add_neighbour_existing():
    vertex = Vertex("A")
    neighbour = Vertex("B")
    vertex.add_neighbour(neighbour, 5)
    vertex.add_neighbour(neighbour, 10)
    assert vertex.get_weight(neighbour) == 10

def test_does_it_point_to_self():
    vertex = Vertex("A")
    vertex.add_neighbour(vertex, 1)
    assert vertex.does_it_point_to(vertex)

def test_get_neighbours_empty():
    vertex = Vertex("A")
    assert not list(vertex.get_neighbours())

def test_get_neighbours_non_empty():
    vertex = Vertex("A")
    neighbour = Vertex("B")
    vertex.add_neighbour(neighbour, 1)
    assert list(vertex.get_neighbours()) == [neighbour]

def test_get_weight_non_existing_neighbour():
    vertex = Vertex("A")
    neighbour = Vertex("B")
    with pytest.raises(KeyError):
        vertex.get_weight(neighbour)

def test_vertex_check_in_graph():
    graph = Graph()
    graph.add_vertex("A")
    assert "A" in graph



def test_dijkstra_edge_weights_original_behavior():
    graph = Graph()
    graph.add_vertex("A")
    graph.add_vertex("B")
    graph.add_edge("A", "B")
    source = graph.get_vertex("A")
    distances = dijkstra(graph, source)
    assert distances[graph.get_vertex("B")] == 1



def test_dijkstra_update_distance_strict_comparison():
    graph = Graph()
    graph.add_vertex("A")
    graph.add_vertex("B")
    graph.add_vertex("C")
    graph.add_edge("A", "B", 5)
    graph.add_edge("B", "C", 3)
    source = graph.get_vertex("A")
    distances = dijkstra(graph, source)
    assert distances[graph.get_vertex("C")] == 8

