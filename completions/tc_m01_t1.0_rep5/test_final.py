
import pytest
from nds_script import Graph, Vertex, dijkstra


def test_add_vertex():
    g = Graph()
    g.add_vertex('A')
    assert 'A' in g

def test_add_edge():
    g = Graph()
    g.add_vertex('A')
    g.add_vertex('B')
    g.add_edge('A', 'B')
    assert g.does_edge_exist('A', 'B')

def test_get_vertex():
    g = Graph()
    g.add_vertex('A')
    assert isinstance(g.get_vertex('A'), Vertex)

def test_vertex_key():
    v = Vertex('A')
    assert v.get_key() == 'A'

def test_add_neighbour():
    v1 = Vertex('A')
    v2 = Vertex('B')
    v1.add_neighbour(v2, 5)
    assert v1.get_weight(v2) == 5

def test_vertex_neighbours():
    v1 = Vertex('A')
    v2 = Vertex('B')
    v1.add_neighbour(v2, 5)
    assert v2 in v1.get_neighbours()

def test_dijkstra_basic():
    g = Graph()
    g.add_vertex('A')
    g.add_vertex('B')
    g.add_edge('A', 'B', 1)
    distances = dijkstra(g, g.get_vertex('A'))
    assert distances[g.get_vertex('B')] == 1

def test_dijkstra_unconnected():
    g = Graph()
    g.add_vertex('A')
    g.add_vertex('B')
    distances = dijkstra(g, g.get_vertex('A'))
    assert distances[g.get_vertex('B')] == float('inf')

# def test_add_vertex_duplicate():
#     g = Graph()
#     g.add_vertex('A')
#     with pytest.raises(Exception):
#         g.add_vertex('A')

def test_add_edge_nonexistent_vertex():
    g = Graph()
    g.add_vertex('A')
    with pytest.raises(Exception):
        g.add_edge('A', 'B')

def test_get_vertex_nonexistent():
    g = Graph()
    with pytest.raises(Exception):
        g.get_vertex('Z')

# def test_add_edge_to_self():
#     g = Graph()
#     g.add_vertex('A')
#     with pytest.raises(Exception):
#         g.add_edge('A', 'A')

# def test_dijkstra_nonexistent_source():
#     g = Graph()
#     g.add_vertex('A')
#     with pytest.raises(Exception):
#         dijkstra(g, Vertex('Z'))

# def test_dijkstra_empty_graph():
#     g = Graph()
#     with pytest.raises(Exception):
#         dijkstra(g, Vertex('A'))

# def test_dijkstra_invalid_source():
#     g = Graph()
#     with pytest.raises(TypeError):
#         dijkstra(g, 'A')

# def test_dijkstra_different_edge_weight():
#     g = Graph()
#     g.add_vertex('A')
#     g.add_vertex('B')
#     g.add_edge('A', 'B')
#     distances = dijkstra(g, g.get_vertex('A'))
#     assert distances[g.get_vertex('B')] == 2  # This will fail in the original because the weight should be 1, so this is designed for mutant
