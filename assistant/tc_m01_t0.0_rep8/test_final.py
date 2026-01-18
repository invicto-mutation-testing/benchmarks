import pytest
from put import Graph, Vertex, dijkstra

@pytest.fixture
def empty_graph():
    return Graph()

@pytest.fixture
def graph_with_vertices():
    g = Graph()
    for key in range(5):
        g.add_vertex(key)
    return g

@pytest.fixture
def graph_with_edges():
    g = Graph()
    for key in range(5):
        g.add_vertex(key)
    edges = [(0, 1, 5), (1, 2, 3), (2, 3, 2), (3, 4, 1), (0, 4, 10)]
    for src, dest, weight in edges:
        g.add_edge(src, dest, weight)
    return g

def test_add_vertex(empty_graph):
    empty_graph.add_vertex(1)
    assert 1 in empty_graph
    assert isinstance(empty_graph.get_vertex(1), Vertex)

def test_add_vertex_duplicate(graph_with_vertices):
    graph_with_vertices.add_vertex(1)  # Adding duplicate
    assert 1 in graph_with_vertices

def test_get_vertex_nonexistent(empty_graph):
    with pytest.raises(KeyError):
        empty_graph.get_vertex(99)

def test_add_edge_nonexistent_vertex(graph_with_vertices):
    with pytest.raises(KeyError):
        graph_with_vertices.add_edge(1, 99)

def test_does_edge_exist(graph_with_edges):
    assert graph_with_edges.does_edge_exist(0, 1)
    assert not graph_with_edges.does_edge_exist(1, 0)

def test_dijkstra_basic(graph_with_edges):
    source = graph_with_edges.get_vertex(0)
    distances = dijkstra(graph_with_edges, source)
    assert distances[source] == 0
    assert distances[graph_with_edges.get_vertex(4)] == 10  # Corrected expected value

def test_dijkstra_unconnected_graph(graph_with_vertices):
    source = graph_with_vertices.get_vertex(0)
    distances = dijkstra(graph_with_vertices, source)
    assert distances[source] == 0
    assert all(distances[v] == float('inf') for v in graph_with_vertices if v != source)

def test_vertex_add_neighbour(graph_with_vertices):
    v1 = graph_with_vertices.get_vertex(1)
    v2 = graph_with_vertices.get_vertex(2)
    v1.add_neighbour(v2, 10)
    assert v1.does_it_point_to(v2)
    assert v1.get_weight(v2) == 10

def test_vertex_get_neighbours(graph_with_edges):
    v1 = graph_with_edges.get_vertex(1)
    neighbours = list(v1.get_neighbours())
    assert len(neighbours) == 1
    assert neighbours[0].get_key() == 2

def test_vertex_get_weight_nonexistent_neighbour(graph_with_vertices):
    v1 = graph_with_vertices.get_vertex(1)
    v2 = graph_with_vertices.get_vertex(2)
    with pytest.raises(KeyError):
        v1.get_weight(v2)

def test_default_edge_weight(graph_with_vertices):
    graph_with_vertices.add_vertex(10)
    graph_with_vertices.add_vertex(20)
    graph_with_vertices.add_edge(10, 20)  # Default weight should be 1 in original code
    v10 = graph_with_vertices.get_vertex(10)
    v20 = graph_with_vertices.get_vertex(20)
    assert v10.get_weight(v20) == 1, "Default weight should be 1, mutation changes it to 2"

# Corrected test case to match the expected behavior in the original code
def test_dijkstra_edge_case(graph_with_edges):
    source = graph_with_edges.get_vertex(0)
    distances = dijkstra(graph_with_edges, source)
    assert distances[graph_with_edges.get_vertex(4)] == 10  # The shortest path should be 0 -> 1 -> 2 -> 3 -> 4 with total weight 11