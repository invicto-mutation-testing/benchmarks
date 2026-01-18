

import pytest
from nds_script import Graph, Vertex, dijkstra


def test_graph_init():
    g = Graph()
    assert isinstance(g, Graph)
    assert g.vertices == {}

def test_vertex_init():
    v = Vertex("A")
    assert v.key == "A"
    assert v.points_to == {}

def test_add_vertex():
    g = Graph()
    g.add_vertex("A")
    assert "A" in g.vertices

def test_get_vertex():
    g = Graph()
    g.add_vertex("A")
    vertex = g.get_vertex("A")
    assert isinstance(vertex, Vertex)
    assert vertex.key == "A"

def test_add_edge():
    g = Graph()
    g.add_vertex("A")
    g.add_vertex("B")
    g.add_edge("A", "B", 5)
    assert g.does_edge_exist("A", "B")

def test_vertex_not_found_add_edge():
    g = Graph()
    g.add_vertex("A")
    with pytest.raises(KeyError):
        g.add_edge("A", "B", 5)

def test_does_edge_exist():
    g = Graph()
    g.add_vertex("A")
    g.add_vertex("B")
    g.add_edge("A", "B", 3)
    assert g.does_edge_exist("A", "B")

def test_does_edge_not_exist():
    g = Graph()
    g.add_vertex("A")
    g.add_vertex("B")
    assert not g.does_edge_exist("A", "B")

def test_add_neighbour():
    g = Graph()
    g.add_vertex("A")
    g.add_vertex("B")
    vertex_a = g.get_vertex("A")
    vertex_b = g.get_vertex("B")
    vertex_a.add_neighbour(vertex_b, 10)
    assert vertex_b in vertex_a.get_neighbours()

def test_get_weight():
    g = Graph()
    g.add_vertex("A")
    g.add_vertex("B")
    vertex_a = g.get_vertex("A")
    vertex_b = g.get_vertex("B")
    vertex_a.add_neighbour(vertex_b, 20)
    assert vertex_a.get_weight(vertex_b) == 20

def test_vertex_pointing():
    g = Graph()
    g.add_vertex("A")
    g.add_vertex("B")
    vertex_a = g.get_vertex("A")
    vertex_b = g.get_vertex("B")
    vertex_a.add_neighbour(vertex_b, 5)
    assert vertex_a.does_it_point_to(vertex_b)

def test_dijkstra_basic():
    g = Graph()
    g.add_vertex("A")
    g.add_vertex("B")
    g.add_edge("A", "B", 1)
    source = g.get_vertex("A")
    distances = dijkstra(g, source)
    assert distances[source] == 0
    assert distances[g.get_vertex("B")] == 1

def test_dijkstra_no_edges():
    g = Graph()
    g.add_vertex("A")
    source = g.get_vertex("A")
    distances = dijkstra(g, source)
    assert distances[source] == 0

def test_dijkstra_unreachable_vertex():
    g = Graph()
    g.add_vertex("A")
    g.add_vertex("B")
    source = g.get_vertex("A")
    distances = dijkstra(g, source)
    assert distances[g.get_vertex("B")] == float('inf')

# def test_dijkstra_invalid_source():
#     g = Graph()
#     g.add_vertex("A")
#     with pytest.raises(KeyError):
#         distances = dijkstra(g, Vertex("B"))

def test_graph_contains():
    g = Graph()
    g.add_vertex("A")
    assert "A" in g
    assert "B" not in g

def test_dijkstra_edge_default_weight():
    g = Graph()
    g.add_vertex("A")
    g.add_vertex("B")
    g.add_edge("A", "B")  # Implicit weight=1 in original, different in mutant
    source = g.get_vertex("A")
    distances = dijkstra(g, source)
    assert distances[source] == 0
    assert distances[g.get_vertex("B")] == 1  # This should fail in mutant as weight would be 2



def test_dijkstra_improved_comparison():
    g = Graph()
    g.add_vertex("A")
    g.add_vertex("B")
    g.add_edge("A", "B", 2)
    g.add_vertex("C")
    g.add_edge("A", "C", 1)
    g.add_edge("C", "B", 1)  # Total distance A -> C -> B = 2
    source = g.get_vertex("A")
    distances = dijkstra(g, source)
    assert distances[g.get_vertex("B")] == 2  # This should fail in mutant with distance being possibly 1 if it doesn't check weights properly

