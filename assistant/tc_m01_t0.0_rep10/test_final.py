import pytest
from put import Graph, Vertex, dijkstra

@pytest.fixture
def empty_graph():
    return Graph()

@pytest.fixture
def graph_with_vertices():
    g = Graph()
    v1 = Vertex('A')
    v2 = Vertex('B')
    v3 = Vertex('C')
    g.vertices['A'] = v1
    g.vertices['B'] = v2
    g.vertices['C'] = v3
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

def test_get_vertex(graph_with_vertices):
    g, v1, v2, v3 = graph_with_vertices
    assert g.get_vertex('A') == v1
    assert g.get_vertex('B') == v2

def test_vertex_not_found(empty_graph):
    with pytest.raises(KeyError):
        empty_graph.get_vertex('Z')

def test_add_edge(graph_with_vertices):
    g, v1, v2, v3 = graph_with_vertices
    g.add_edge('A', 'B', 1)
    assert g.does_edge_exist('A', 'B')

def test_add_edge_invalid_vertex(empty_graph):
    empty_graph.add_vertex('A')
    with pytest.raises(KeyError):
        empty_graph.add_edge('A', 'B', 1)

def test_does_edge_exist(graph_with_edges):
    g, v1, v2, v3 = graph_with_edges
    assert g.does_edge_exist('A', 'B')
    assert not g.does_edge_exist('C', 'A')

def test_dijkstra_basic(graph_with_edges):
    g, v1, v2, v3 = graph_with_edges
    distances = dijkstra(g, v1)
    assert distances[v1] == 0
    assert distances[v2] == 1
    assert distances[v3] == 3

def test_dijkstra_unconnected_graph(graph_with_vertices):
    g, v1, v2, v3 = graph_with_vertices
    distances = dijkstra(g, v1)
    assert distances[v1] == 0
    assert distances[v2] == float('inf')
    assert distances[v3] == float('inf')

def test_iter_graph(graph_with_vertices):
    g, v1, v2, v3 = graph_with_vertices
    vertices = list(iter(g))
    assert set(vertices) == {v1, v2, v3}

def test_default_edge_weight(graph_with_vertices):
    g, v1, v2, v3 = graph_with_vertices
    g.add_edge('A', 'B')  # No weight specified, should default to 1 in original code
    assert g.get_vertex('A').get_weight(g.get_vertex('B')) == 1, "Default weight should be 1 as per original code"

def test_vertex_initialization():
    v = Vertex('A')
    assert v.get_key() is not None, "Vertex key should not be None after initialization with a valid key"

def test_vertex_key_assignment():
    v = Vertex('A')
    assert v.get_key() == 'A', "Vertex key should be 'A' when initialized with 'A'"

# New test case to catch the mutation
def test_dijkstra_edge_case(graph_with_edges):
    g, v1, v2, v3 = graph_with_edges
    # Adding an edge with the same weight as an existing shortest path
    g.add_edge('B', 'A', 1)  # This creates a cycle with equal weight
    distances = dijkstra(g, v1)
    # In the original code, this should not change the shortest path to B
    assert distances[v2] == 1, "Distance to B should remain 1"
    # In the mutated code, this might incorrectly update the distance to B