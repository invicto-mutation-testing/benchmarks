import pytest
from put import Graph, Vertex, dijkstra

@pytest.fixture
def empty_graph():
    return Graph()

@pytest.fixture
def graph_with_vertices():
    g = Graph()
    for key in ['A', 'B', 'C', 'D']:
        g.add_vertex(key)
    return g

@pytest.fixture
def graph_with_edges(graph_with_vertices):
    g = graph_with_vertices
    g.add_edge('A', 'B', 1)
    g.add_edge('A', 'C', 3)
    g.add_edge('B', 'C', 1)
    g.add_edge('C', 'D', 2)
    g.add_edge('D', 'A', 4)
    return g

def test_dijkstra_basic(graph_with_edges):
    source = graph_with_edges.get_vertex('A')
    distances = dijkstra(graph_with_edges, source)
    expected = {'A': 0, 'B': 1, 'C': 2, 'D': 4}
    # Fixing the assertion to compare keys instead of vertex objects
    assert {v.get_key(): distances[v] for v in distances} == expected

def test_add_vertex(empty_graph):
    empty_graph.add_vertex('A')
    assert 'A' in empty_graph
    assert isinstance(empty_graph.get_vertex('A'), Vertex)

def test_get_vertex_nonexistent(empty_graph):
    with pytest.raises(KeyError):
        empty_graph.get_vertex('Z')

def test_add_edge_nonexistent_vertex(graph_with_vertices):
    with pytest.raises(KeyError):
        graph_with_vertices.add_edge('A', 'Z')

def test_does_edge_exist(graph_with_edges):
    assert graph_with_edges.does_edge_exist('A', 'B')
    assert not graph_with_edges.does_edge_exist('A', 'D')

def test_vertex_add_neighbour(graph_with_vertices):
    v1 = graph_with_vertices.get_vertex('A')
    v2 = graph_with_vertices.get_vertex('B')
    v1.add_neighbour(v2, 5)
    assert v1.does_it_point_to(v2)
    assert v1.get_weight(v2) == 5

def test_vertex_get_neighbours(graph_with_edges):
    v = graph_with_edges.get_vertex('A')
    neighbours = v.get_neighbours()
    assert set(neighbour.get_key() for neighbour in neighbours) == {'B', 'C'}

def test_vertex_get_weight_nonexistent_neighbour(graph_with_vertices):
    v1 = graph_with_vertices.get_vertex('A')
    v2 = graph_with_vertices.get_vertex('B')
    with pytest.raises(KeyError):
        v1.get_weight(v2)

def test_default_edge_weight(graph_with_vertices):
    graph_with_vertices.add_edge('A', 'B')  # No weight specified, should default to 1
    v1 = graph_with_vertices.get_vertex('A')
    v2 = graph_with_vertices.get_vertex('B')
    assert v1.get_weight(v2) == 1, "Default weight should be 1, mutation changes it to 2"

# New test case to catch the mutation in the dijkstra function
def test_dijkstra_edge_case(graph_with_edges):
    source = graph_with_edges.get_vertex('A')
    distances = dijkstra(graph_with_edges, source)
    expected = {'A': 0, 'B': 1, 'C': 2, 'D': 4}
    # This test will pass in the original code and fail in the mutated code due to the change in the comparison operator
    assert {v.get_key(): distances[v] for v in distances} == expected