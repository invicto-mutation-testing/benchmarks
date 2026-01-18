

import pytest
from nds_script import Graph, Vertex, dijkstra


def test_graph_initialization():
    g = Graph()
    assert isinstance(g, Graph)
    assert g.vertices == {}

def test_vertex_initialization():
    v = Vertex('A')
    assert isinstance(v, Vertex)
    assert v.key == 'A'
    assert v.points_to == {}

def test_add_vertex():
    g = Graph()
    g.add_vertex('A')
    assert 'A' in g.vertices
    assert isinstance(g.vertices['A'], Vertex)

def test_get_vertex():
    g = Graph()
    g.add_vertex('A')
    vertex = g.get_vertex('A')
    assert vertex == g.vertices['A']

def test_get_vertex_nonexistent():
    g = Graph()
    with pytest.raises(KeyError):
        g.get_vertex('NonExistent')

def test_add_edge():
    g = Graph()
    g.add_vertex('A')
    g.add_vertex('B')
    g.add_edge('A', 'B', 10)
    assert g.vertices['A'].points_to == {g.vertices['B']: 10}

def test_add_edge_nonexistent_vertices():
    g = Graph()
    g.add_vertex('A')
    with pytest.raises(KeyError):
        g.add_edge('A', 'B', 10)

def test_does_edge_exist():
    g = Graph()
    g.add_vertex('A')
    g.add_vertex('B')
    assert not g.does_edge_exist('A', 'B')
    g.add_edge('A', 'B')
    assert g.does_edge_exist('A', 'B')

def test_dijkstra_algorithm():
    g = Graph()
    nodes = ['A', 'B', 'C']
    for node in nodes:
        g.add_vertex(node)
    g.add_edge('A', 'B', 1)
    g.add_edge('B', 'C', 2)
    g.add_edge('A', 'C', 4)
    source = g.get_vertex('A')
    distances = dijkstra(g, source)
    assert distances[g.get_vertex('A')] == 0
    assert distances[g.get_vertex('B')] == 1
    assert distances[g.get_vertex('C')] == 3  # A -> B -> C

def test_dijkstra_unconnected():
    g = Graph()
    g.add_vertex('A')
    g.add_vertex('B')
    source = g.get_vertex('A')
    distances = dijkstra(g, source)
    assert distances[g.get_vertex('A')] == 0
    assert distances[g.get_vertex('B')] == float('inf')

# def test_dijkstra_invalid_source():
#     g = Graph()
#     g.add_vertex('A')
#     with pytest.raises(KeyError):
#         dijkstra(g, 'NonExistent')

def test_vertex_does_it_point_to():
    g = Graph()
    g.add_vertex('A')
    g.add_vertex('B')
    v = g.get_vertex('A')
    assert not v.does_it_point_to(g.get_vertex('B'))
    v.add_neighbour(g.get_vertex('B'), 10)
    assert v.does_it_point_to(g.get_vertex('B'))

def test_vertex_get_key():
    v = Vertex('X')
    assert v.get_key() == 'X'

def test_vertex_get_weight():
    g = Graph()
    g.add_vertex('A')
    g.add_vertex('B')
    v = g.get_vertex('A')
    v.add_neighbour(g.get_vertex('B'), 5)
    assert v.get_weight(g.get_vertex('B')) == 5

def test_vertex_get_weight_nonexistent():
    v = Vertex('A')
    b = Vertex('B')
    with pytest.raises(KeyError):
        v.get_weight(b)

def test_vertex_get_neighbours():
    g = Graph()
    g.add_vertex('A')
    g.add_vertex('B')
    v = g.get_vertex('A')
    v.add_neighbour(g.get_vertex('B'), 10)
    assert g.get_vertex('B') in list(v.get_neighbours())

def test_graph_contains():
    g = Graph()
    g.add_vertex('A')
    assert 'A' in g



def test_add_edge_default_weight():
    g = Graph()
    g.add_vertex('A')
    g.add_vertex('B')
    g.add_edge('A', 'B')  # default weight should be 1 in original
    assert g.vertices['A'].points_to[g.vertices['B']] == 1



def test_dijkstra_minimum_edge_constraint():
    g = Graph()
    nodes = ['A', 'B', 'C', 'D']
    for node in nodes:
        g.add_vertex(node)
    g.add_edge('A', 'B', 1)
    g.add_edge('B', 'C', 2)
    g.add_edge('A', 'C', 50)
    g.add_edge('C', 'D', 1)
    source = g.get_vertex('A')
    distances = dijkstra(g, source)
    assert distances[g.get_vertex('C')] == 3 # A -> B -> C (Original should pass, Mutant should fail since it might use direct A->C with weight 50)

