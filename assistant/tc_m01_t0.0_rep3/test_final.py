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
    v1.add_neighbour(v2, 1)
    v2.add_neighbour(v3, 2)
    v3.add_neighbour(v1, 3)
    return g, v1, v2, v3

def test_add_vertex(empty_graph):
    empty_graph.add_vertex('A')
    assert 'A' in empty_graph
    assert isinstance(empty_graph.get_vertex('A'), Vertex)

def test_get_vertex(graph_with_vertices):
    g, v1, v2, v3 = graph_with_vertices
    assert g.get_vertex('A') == v1
    assert g.get_vertex('B') == v2
    assert g.get_vertex('C') == v3

def test_add_edge(graph_with_vertices):
    g, v1, v2, v3 = graph_with_vertices
    g.add_edge('A', 'B', 5)
    assert g.does_edge_exist('A', 'B')
    assert not g.does_edge_exist('B', 'A')

def test_dijkstra_basic(graph_with_edges):
    g, v1, v2, v3 = graph_with_edges
    distances = dijkstra(g, v1)
    assert distances[v1] == 0
    assert distances[v2] == 1
    assert distances[v3] == 3

def test_dijkstra_unreachable(graph_with_vertices):
    g, v1, v2, v3 = graph_with_vertices
    distances = dijkstra(g, v1)
    assert distances[v1] == 0
    assert distances[v2] == float('inf')
    assert distances[v3] == float('inf')

def test_vertex_not_in_graph(empty_graph):
    with pytest.raises(KeyError):
        empty_graph.get_vertex('Z')

def test_edge_not_in_graph(graph_with_vertices):
    g, v1, v2, v3 = graph_with_vertices
    with pytest.raises(KeyError):
        g.add_edge('A', 'Z')

def test_add_edge_to_nonexistent_vertex(graph_with_vertices):
    g, v1, v2, v3 = graph_with_vertices
    with pytest.raises(KeyError):
        g.add_edge('A', 'D')

def test_default_edge_weight(graph_with_vertices):
    g, v1, v2, v3 = graph_with_vertices
    g.add_edge('A', 'B')  # Default weight should be 1 in the original code
    assert v1.get_weight(v2) == 1, "Default weight should be 1, mutation changed it to 2"

# New test case to catch the mutation
def test_dijkstra_edge_case(graph_with_vertices):
    g, v1, v2, v3 = graph_with_vertices
    g.add_edge('A', 'B', 1)
    g.add_edge('B', 'C', 1)
    g.add_edge('C', 'A', 1)
    distances = dijkstra(g, v1)
    assert distances[v2] == 1, "Distance to B should be 1"
    assert distances[v3] == 2, "Distance to C should be 2, mutation may cause incorrect distance calculation"