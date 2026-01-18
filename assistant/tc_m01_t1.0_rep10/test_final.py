import pytest
from put import Graph, Vertex, dijkstra

@pytest.fixture
def empty_graph():
    """Fixture to provide an empty Graph instance."""
    return Graph()

@pytest.fixture
def graph_with_vertices():
    """Fixture to provide a Graph instance populated with vertices but no edges."""
    g = Graph()
    for key in ['A', 'B', 'C']:
        g.add_vertex(key)
    return g

@pytest.fixture
def graph_with_edges():
    """Fixture to provide a Graph instance with vertices and edges."""
    g = Graph()
    # Adding vertices
    for key in ['A', 'B', 'C']:
        g.add_vertex(key)
    # Adding edges
    g.add_edge('A', 'B', 1)
    g.add_edge('B', 'C', 2)
    g.add_edge('A', 'C', 3)
    return g

def test_add_vertex(empty_graph):
    empty_graph.add_vertex('A')
    assert 'A' in empty_graph
    assert isinstance(empty_graph.get_vertex('A'), Vertex)

def test_get_vertex_exception(empty_graph):
    with pytest.raises(KeyError):
        empty_graph.get_vertex('A')

def test_add_edge(graph_with_vertices):
    graph_with_vertices.add_edge('A', 'B', 1)
    assert graph_with_vertices.does_edge_exist('A', 'B')

def test_add_edge_exception_source_not_present(graph_with_vertices):
    with pytest.raises(KeyError):
        graph_with_vertices.add_edge('X', 'B', 2)

def test_add_edge_exception_destination_not_present(graph_with_vertices):
    with pytest.raises(KeyError):
        graph_with_vertices.add_edge('A', 'X', 2)

def test_does_edge_exist(graph_with_edges):
    assert graph_with_edges.does_edge_exist('A', 'B')
    with pytest.raises(KeyError):
        graph_with_edges.does_edge_exist('A', 'D')  # A to D does not exist

def test_iterate_vertices(graph_with_edges):
    keys = [v.get_key() for v in graph_with_edges]
    assert sorted(keys) == ['A', 'B', 'C']

def test_dijkstra_basic(graph_with_edges):
    source = graph_with_edges.get_vertex('A')
    distances = dijkstra(graph_with_edges, source)
    assert distances[source] == 0
    assert distances[graph_with_edges.get_vertex('B')] == 1
    assert distances[graph_with_edges.get_vertex('C')] == 3

def test_dijkstra_unconnected_graph(graph_with_vertices):
    source = graph_with_vertices.get_vertex('A')
    distances = dijkstra(graph_with_vertices, source)
    assert distances[source] == 0
    assert distances[graph_with_vertices.get_vertex('B')] == float('inf')

# New test case to capture the mutation
def test_add_edge_default_weight(graph_with_vertices):
    """Test the default edge weight."""
    graph_with_vertices.add_edge('A', 'B')  # By default should add with weight=1 in original, 2 in mutant
    assert graph_with_vertices.does_edge_exist('A', 'B')
    b_vertex = graph_with_vertices.get_vertex('B')
    a_vertex = graph_with_vertices.get_vertex('A')
    assert a_vertex.get_weight(b_vertex) == 1  # This asserts original weight of 1 is used