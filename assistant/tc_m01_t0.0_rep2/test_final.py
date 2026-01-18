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
    edges = [(0, 1, 10), (1, 2, 20), (2, 3, 30), (3, 4, 40), (4, 0, 50)]
    for src, dest, weight in edges:
        g.add_edge(src, dest, weight)
    return g

def test_add_vertex(empty_graph):
    empty_graph.add_vertex(1)
    assert 1 in empty_graph
    assert isinstance(empty_graph.get_vertex(1), Vertex)

def test_add_vertex_duplicate(graph_with_vertices):
    graph_with_vertices.add_vertex(1)  # Adding the same vertex again
    assert 1 in graph_with_vertices  # The vertex should still exist
    assert len(graph_with_vertices.vertices) == 5  # No new vertex should be added

def test_get_vertex_nonexistent(empty_graph):
    with pytest.raises(KeyError):
        empty_graph.get_vertex(100)

def test_add_edge_nonexistent_vertex(graph_with_vertices):
    with pytest.raises(KeyError):
        graph_with_vertices.add_edge(1, 100)

def test_does_edge_exist(graph_with_edges):
    assert graph_with_edges.does_edge_exist(0, 1)
    assert not graph_with_edges.does_edge_exist(0, 2)

def test_dijkstra_basic(graph_with_edges):
    source = graph_with_edges.get_vertex(0)
    distances = dijkstra(graph_with_edges, source)
    assert distances[source] == 0
    assert distances[graph_with_edges.get_vertex(1)] == 10
    assert distances[graph_with_edges.get_vertex(2)] == 30
    assert distances[graph_with_edges.get_vertex(3)] == 60
    assert distances[graph_with_edges.get_vertex(4)] == 100

def test_dijkstra_unconnected_graph(graph_with_vertices):
    source = graph_with_vertices.get_vertex(0)
    distances = dijkstra(graph_with_vertices, source)
    assert distances[source] == 0
    for key in range(1, 5):
        assert distances[graph_with_vertices.get_vertex(key)] == float('inf')

def test_vertex_add_neighbour(graph_with_vertices):
    v1 = graph_with_vertices.get_vertex(1)
    v2 = graph_with_vertices.get_vertex(2)
    v1.add_neighbour(v2, 5)
    assert v1.does_it_point_to(v2)
    assert v1.get_weight(v2) == 5

def test_vertex_get_neighbours(graph_with_vertices):
    v1 = graph_with_vertices.get_vertex(1)
    v2 = graph_with_vertices.get_vertex(2)
    v3 = graph_with_vertices.get_vertex(3)
    v1.add_neighbour(v2, 5)
    v1.add_neighbour(v3, 10)
    neighbours = list(v1.get_neighbours())
    assert v2 in neighbours
    assert v3 in neighbours
    assert len(neighbours) == 2

def test_vertex_get_weight_nonexistent_neighbour(graph_with_vertices):
    v1 = graph_with_vertices.get_vertex(1)
    v2 = graph_with_vertices.get_vertex(2)
    with pytest.raises(KeyError):
        v1.get_weight(v2)

# New test case to catch the mutation
def test_vertex_initialization_key():
    # This test will pass in the original code and fail in the mutated code
    # because in the original code, the vertex key is correctly initialized,
    # but in the mutated code, it is incorrectly set to None.
    v = Vertex(1)
    assert v.get_key() == 1