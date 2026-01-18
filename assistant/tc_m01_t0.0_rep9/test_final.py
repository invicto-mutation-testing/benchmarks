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
    edges = [(0, 1, 2), (1, 2, 3), (2, 3, 4), (3, 4, 5), (4, 0, 1)]
    for src, dest, weight in edges:
        g.add_edge(src, dest, weight)
    return g

def test_add_vertex(empty_graph):
    empty_graph.add_vertex(1)
    assert 1 in empty_graph
    assert isinstance(empty_graph.get_vertex(1), Vertex)

def test_add_edge(graph_with_vertices):
    graph_with_vertices.add_edge(0, 1, 10)
    assert graph_with_vertices.does_edge_exist(0, 1)
    assert graph_with_vertices.get_vertex(0).get_weight(graph_with_vertices.get_vertex(1)) == 10

def test_get_vertex_nonexistent(empty_graph):
    with pytest.raises(KeyError):
        empty_graph.get_vertex(99)

def test_add_edge_nonexistent_vertex(graph_with_vertices):
    with pytest.raises(KeyError):
        graph_with_vertices.add_edge(0, 99, 10)

def test_dijkstra_basic(graph_with_edges):
    source = graph_with_edges.get_vertex(0)
    distances = dijkstra(graph_with_edges, source)
    assert distances[source] == 0
    assert distances[graph_with_edges.get_vertex(1)] == 2
    assert distances[graph_with_edges.get_vertex(2)] == 5
    assert distances[graph_with_edges.get_vertex(3)] == 9
    assert distances[graph_with_edges.get_vertex(4)] == 14

def test_dijkstra_unconnected_graph(graph_with_vertices):
    source = graph_with_vertices.get_vertex(0)
    distances = dijkstra(graph_with_vertices, source)
    assert distances[source] == 0
    for key in range(1, 5):
        assert distances[graph_with_vertices.get_vertex(key)] == float('inf')

def test_vertex_add_neighbour(graph_with_vertices):
    vertex0 = graph_with_vertices.get_vertex(0)
    vertex1 = graph_with_vertices.get_vertex(1)
    vertex0.add_neighbour(vertex1, 5)
    assert vertex0.does_it_point_to(vertex1)
    assert vertex0.get_weight(vertex1) == 5

def test_vertex_nonexistent_neighbour(graph_with_vertices):
    vertex0 = graph_with_vertices.get_vertex(0)
    vertex1 = Vertex(99)  # Non-existent vertex
    with pytest.raises(KeyError):
        vertex0.get_weight(vertex1)

def test_default_edge_weight(graph_with_vertices):
    graph_with_vertices.add_edge(0, 1)
    assert graph_with_vertices.get_vertex(0).get_weight(graph_with_vertices.get_vertex(1)) == 1, "Default weight should be 1 as per original code"

# New test case to catch mutation
def test_vertex_initialization_key(graph_with_vertices):
    vertex = graph_with_vertices.get_vertex(0)
    assert vertex.get_key() is not None, "Vertex key should not be None after initialization"

def test_vertex_initialization_key_correctness(graph_with_vertices):
    vertex = graph_with_vertices.get_vertex(0)
    assert vertex.get_key() == 0, "Vertex key should be correctly initialized to the value passed to constructor"