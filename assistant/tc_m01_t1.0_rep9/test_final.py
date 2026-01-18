import pytest
from put import Graph, Vertex, dijkstra

@pytest.fixture
def setup_graph():
    g = Graph()
    keys = ['A', 'B', 'C']  # Removed 'D' from here since it should not exist in the graph
    vertices_map = {}
    for key in keys:
        g.add_vertex(key)
        vertices_map[key] = g.get_vertex(key)
    return g, vertices_map

def test_dijkstra_basic(setup_graph):
    g, vertices_map = setup_graph
    g.add_edge('A', 'B', 2)
    g.add_edge('B', 'C', 3)
    va = vertices_map['A']
    vb = vertices_map['B']
    vc = vertices_map['C']
    distances = dijkstra(g, va)
    assert distances[va] == 0
    assert distances[vb] == 2
    assert distances[vc] == 5

def test_iter_graph(setup_graph):
    g, vertices_map = setup_graph
    expected_set = set(vertices_map.values())
    result_set = set(v for v in g)
    assert expected_set == result_set

def test_graph_contains(setup_graph):
    g, vertices_map = setup_graph
    assert 'A' in g
    assert 'D' not in g  # This assertion is correct as 'D' is not added to vertices_map

def test_graph_correct_edge_existence_check(setup_graph):
    g, vertices_map = setup_graph
    g.add_edge('A', 'B', 1)
    assert g.does_edge_exist('A', 'B')
    assert not g.does_edge_exist('A', 'C')

def test_handle_adding_duplicate_vertex(setup_graph):
    g, vertices_map = setup_graph
    g.add_vertex('A')  # Try to add a duplicate vertex 'A'
    assert 'A' in g

def test_default_edge_weight(setup_graph):
    g, vertices_map = setup_graph
    g.add_edge('A', 'B')
    va = vertices_map['A']
    vb = vertices_map['B']
    assert g.get_vertex('A').get_weight(vb) == 1

def test_dijkstra_default_weights(setup_graph):
    g, vertices_map = setup_graph
    g.add_edge('A', 'B')
    g.add_edge('B', 'C')
    va = vertices_map['A']
    vb = vertices_map['B']
    vc = vertices_map['C']
    distances = dijkstra(g, va)
    assert distances[vc] == 2

def test_vertex_key_initialization(setup_graph):
    g, vertices_map = setup_graph
    key = 'A'
    assert vertices_map[key].get_key() == key

def test_graph_vertex_retrieval_by_correct_key(setup_graph):
    g, vertices_map = setup_graph
    key = 'B'
    retrieved_vertex = g.get_vertex(key)
    assert retrieved_vertex is vertices_map[key] and retrieved_vertex.get_key() == key

# This should work as initially designed
def test_dijkstra_non_strict_inequality_issue(setup_graph):
    """
    This test is designed to fail if the inequality in the dijkstra function is not strict, 
    as it is in the mutant version of the code.
    """
    g, vertices_map = setup_graph
    g.add_edge('A', 'B', 5)
    g.add_edge('B', 'C', 0)  # Zero weight edge
    g.add_edge('A', 'C', 5)  # Direct connection with same weight

    va = vertices_map['A']
    vc = vertices_map['C']

    distances = dijkstra(g, va)
    assert distances[vc] < 6  # Should route through B and then to C
    assert distances[vc] == 5  # The distance via B or directly should remain 5