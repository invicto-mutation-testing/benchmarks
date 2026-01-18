import pytest
from put import Graph, Vertex, dijkstra

@pytest.fixture
def empty_graph():
    return Graph()

@pytest.fixture
def graph_and_vertices():
    g = Graph()
    v1 = Vertex('A')
    v2 = Vertex('B')
    v3 = Vertex('C')
    g.add_vertex('A')
    g.add_vertex('B')
    g.add_vertex('C')
    g.vertices['A'] = v1
    g.vertices['B'] = v2
    g.vertices['C'] = v3
    return g, v1, v2, v3

def test_add_vertex(empty_graph):
    empty_graph.add_vertex('A')
    assert 'A' in empty_graph
    assert isinstance(empty_graph.get_vertex('A'), Vertex)

def test_get_vertex(graph_and_vertices):
    g, v1, _, _ = graph_and_vertices
    assert g.get_vertex('A') == v1

def test_get_vertex_nonexistent(empty_graph):
    with pytest.raises(KeyError):
        empty_graph.get_vertex('Nonexistent')

def test_add_edge(graph_and_vertices):
    g, v1, v2, _ = graph_and_vertices
    g.add_edge('A', 'B', 3)
    assert g.does_edge_exist('A', 'B')
    assert v1.get_weight(v2) == 3

def test_add_edge_nonexistent_vertex(empty_graph):
    empty_graph.add_vertex('A')
    with pytest.raises(KeyError):
        empty_graph.add_edge('A', 'Nonexistent')

def test_dijkstra_basic(graph_and_vertices):
    g, v1, v2, v3 = graph_and_vertices
    g.add_edge('A', 'B', 1)
    g.add_edge('B', 'C', 2)
    distances = dijkstra(g, v1)
    assert distances[v2] == 1
    assert distances[v3] == 3

def test_dijkstra_unreachable_vertex(graph_and_vertices):
    g, v1, v2, v3 = graph_and_vertices
    g.add_edge('A', 'B', 1)
    distances = dijkstra(g, v1)
    assert distances[v3] == float('inf')

def test_dijkstra_no_edges(empty_graph):
    v = Vertex('A')
    empty_graph.add_vertex('A')
    distances = dijkstra(empty_graph, v)
    assert distances[v] == 0

def test_dijkstra_with_self_loop(graph_and_vertices):
    g, v1, _, _ = graph_and_vertices
    g.add_edge('A', 'A', 1)
    distances = dijkstra(g, v1)
    assert distances[v1] == 0

def test_default_edge_weight(graph_and_vertices):
    g, v1, v2, _ = graph_and_vertices
    g.add_edge('A', 'B')
    assert v1.get_weight(v2) == 1, "Default weight should be 1 in original code"

def test_vertex_initial_key_assignment(graph_and_vertices):
    _, v1, _, _ = graph_and_vertices
    assert v1.get_key() == 'A', "Vertex key should be initialized as 'A'"

def test_vertex_key_none_issue():
    v = Vertex('Test')
    assert v.get_key() is not None, "Vertex key should not be None after initialization"

# New test cases to catch mutation
def test_incorrect_update_policy_dijkstra(graph_and_vertices):
    """
    Test that the mutation in updating the distance does not affect the original logic of considering an edge only when it strictly improves the distance.
    """
    g, v1, v2, v3 = graph_and_vertices
    g.add_edge('A', 'B', 0)  # zero-weight edge
    g.add_edge('B', 'C', 1)
    g.add_edge('A', 'C', 2)  # direct but not the shortest path initially considered by the mutation
    distances = dijkstra(g, v1)
    
    assert distances[v3] == 1, "The distance should update to 1 via B, not stay 2 despite direct path"