import pytest
from put import Graph, Vertex, dijkstra  # Assuming all classes and functions are in the module 'put'

@pytest.fixture
def empty_graph():
    return Graph()

@pytest.fixture
def graph_with_vertices():
    g = Graph()
    v1 = Vertex('A')
    v2 = Vertex('B')
    v3 = Vertex('C')
    g.add_vertex(v1.get_key())
    g.add_vertex(v2.get_key())
    g.add_vertex(v3.get_key())
    return g, g.get_vertex('A'), g.get_vertex('B'), g.get_vertex('C')  # Ensure getting vertex from graph

@pytest.fixture
def graph_with_edges(graph_with_vertices):
    g, v1, v2, v3 = graph_with_vertices
    g.add_edge('A', 'B', 10)
    g.add_edge('B', 'C', 5)
    g.add_edge('A', 'C', 15)
    return g, v1, v2, v3

def test_get_vertex(graph_with_vertices):
    g, v1, v2, v3 = graph_with_vertices
    assert g.get_vertex('A') is v1
    assert g.get_vertex('B') is v2
    assert g.get_vertex('C') is v3

def test_dijkstra_initial_distances(graph_with_edges):
    g, v1, v2, v3 = graph_with_edges
    distances = dijkstra(g, v1)
    assert distances[v1] == 0
    assert distances[v2] == 10
    assert distances[v3] == 15

def test_dijkstra_complete(graph_with_edges):
    g, v1, _, v3 = graph_with_edges
    distances = dijkstra(g, v1)
    weight_a_c = g.get_vertex('A').get_weight(g.get_vertex('C'))
    assert distances[v3] <= distances[v1] + weight_a_c

def test_dijkstra_missing_vertex(graph_with_vertices):
    g, _, _, _ = graph_with_vertices
    v4 = Vertex('D')
    with pytest.raises(KeyError):
        dijkstra(g, g.get_vertex('D'))

def test_add_vertex(empty_graph):
    empty_graph.add_vertex('D')
    assert 'D' in empty_graph

def test_graph_contains(graph_with_vertices):
    g, v1, v2, v3 = graph_with_vertices
    assert 'A' in g
    assert 'D' not in g

def test_add_edge(graph_with_vertices):
    g, _, _, _ = graph_with_vertices
    g.add_edge('A', 'B', 1)
    assert g.does_edge_exist('A', 'B')
    
def test_invalid_add_edge(empty_graph):
    with pytest.raises(KeyError):
        empty_graph.add_edge('A', 'B')

def test_does_edge_exist(graph_with_edges):
    g, v1, v2, v3 = graph_with_edges
    assert g.does_edge_exist('A', 'B')
    assert not g.does_edge_exist('C', 'A')

def test_iter(graph_with_vertices):
    g, _, _, _ = graph_with_vertices
    keys = [vertex.get_key() for vertex in g]
    assert 'A' in keys
    assert 'B' in keys
    assert 'C' in keys

def test_default_edge_weight(graph_with_vertices):
    g, v1, v2, _ = graph_with_vertices
    g.add_edge('A', 'B')
    assert g.get_vertex('A').get_weight(g.get_vertex('B')) == 1  # Original code had default weight 1

def test_mutation_test_for_edge_weight(graph_with_vertices):
    g, v1, _, _ = graph_with_vertices
    g.add_edge('A', 'B', 1)
    assert g.get_vertex('A').get_weight(g.get_vertex('B')) == 1, "Expected edge weight is 1, received different weight."

# Mutation-specific test cases
def test_dijkstra_should_not_update_if_not_strictly_better(graph_with_edges):
    g, v1, v2, v3 = graph_with_edges
    # Force the mutation condition to hold
    g.add_edge('B', 'C', 15)  # Create a non-optimal path where change can be sensitive
    distances = dijkstra(g, v1)
    # With the mutation, it would incorrectly update C's distance via the worse path from A->B->C
    assert distances[v3] > distances[v2], "Mutation code potentially allows non-better path to influence shortest path calculation."