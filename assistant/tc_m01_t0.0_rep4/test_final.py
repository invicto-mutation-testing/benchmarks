import pytest
from put import Graph, Vertex, dijkstra

@pytest.fixture
def empty_graph():
    return Graph()

@pytest.fixture
def graph_with_vertices():
    g = Graph()
    g.add_vertex('A')
    g.add_vertex('B')
    g.add_vertex('C')
    v1 = g.get_vertex('A')
    v2 = g.get_vertex('B')
    v3 = g.get_vertex('C')
    return g, v1, v2, v3

@pytest.fixture
def graph_with_edges(graph_with_vertices):
    g, v1, v2, v3 = graph_with_vertices
    g.add_edge('A', 'B', 1)
    g.add_edge('B', 'C', 2)
    g.add_edge('A', 'C', 4)
    return g, v1, v2, v3

def test_add_vertex(empty_graph):
    empty_graph.add_vertex('A')
    assert 'A' in empty_graph
    assert isinstance(empty_graph.get_vertex('A'), Vertex)

def test_add_edge(graph_with_vertices):
    g, v1, v2, _ = graph_with_vertices
    g.add_edge('A', 'B', 1)
    assert g.does_edge_exist('A', 'B')
    assert not g.does_edge_exist('B', 'A')

def test_get_vertex(graph_with_vertices):
    g, v1, v2, _ = graph_with_vertices
    assert g.get_vertex('A') == v1
    assert g.get_vertex('B') == v2

def test_vertex_not_found(empty_graph):
    with pytest.raises(KeyError):
        empty_graph.get_vertex('Z')

def test_add_edge_nonexistent_vertex(graph_with_vertices):
    g, _, _, _ = graph_with_vertices
    with pytest.raises(KeyError):
        g.add_edge('A', 'Z', 1)

def test_dijkstra_basic(graph_with_edges):
    g, v1, v2, v3 = graph_with_edges
    distances = dijkstra(g, v1)
    assert distances[v1] == 0
    assert distances[v2] == 1
    assert distances[v3] == 3

def test_dijkstra_unconnected_vertex(graph_with_vertices):
    g, v1, v2, v3 = graph_with_vertices
    distances = dijkstra(g, v1)
    assert distances[v1] == 0
    assert distances[v2] == float('inf')
    assert distances[v3] == float('inf')

def test_dijkstra_empty_graph(empty_graph):
    v = Vertex('A')
    empty_graph.add_vertex('A')
    distances = dijkstra(empty_graph, empty_graph.get_vertex('A'))
    assert distances[empty_graph.get_vertex('A')] == 0

def test_dijkstra_non_member_source(graph_with_vertices):
    g, _, _, _ = graph_with_vertices
    non_member_vertex = Vertex('Z')
    assert non_member_vertex not in g

def test_iter_graph(graph_with_vertices):
    g, v1, v2, v3 = graph_with_vertices
    vertices = list(iter(g))
    assert set(vertices) == {v1, v2, v3}

def test_vertex_add_neighbour(graph_with_vertices):
    _, v1, v2, _ = graph_with_vertices
    v1.add_neighbour(v2, 5)
    assert v1.does_it_point_to(v2)
    assert v1.get_weight(v2) == 5
    assert v2 in v1.get_neighbours()

def test_default_edge_weight(graph_with_vertices):
    g, v1, v2, _ = graph_with_vertices
    g.add_edge('A', 'B')  # No weight specified, should use default of 1
    assert v1.get_weight(v2) == 1  # This will pass in original and fail in mutant

def test_edge_weight_specified(graph_with_vertices):
    g, v1, v2, _ = graph_with_vertices
    g.add_edge('A', 'B', 3)  # Weight explicitly specified
    assert v1.get_weight(v2) == 3  # This will pass in both original and mutant

# New test case to catch the mutation
def test_vertex_initialization(graph_with_vertices):
    g, v1, v2, v3 = graph_with_vertices
    assert v1.get_key() is not None  # This will pass in original and fail in mutant where key is set to None
    assert v2.get_key() is not None
    assert v3.get_key() is not None

# Corrected test to catch the mutation in the dijkstra function
def test_dijkstra_edge_case(graph_with_edges):
    g, v1, v2, v3 = graph_with_edges
    g.add_edge('B', 'A', 1)  # Adding reverse edge to create a cycle
    distances = dijkstra(g, v1)
    assert distances[v2] == 1  # This will pass in original and fail in mutant where the condition is changed
    assert distances[v1] == 0  # Corrected assertion to match the expected behavior