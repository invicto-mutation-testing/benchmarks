

import pytest
from nds_script import Graph, Vertex, dijkstra


def test_graph_init():
    g = Graph()
    assert isinstance(g, Graph)
    assert isinstance(g.vertices, dict)
    assert g.vertices == {}

def test_vertex_init():
    v = Vertex("A")
    assert isinstance(v, Vertex)
    assert v.key == "A"
    assert v.points_to == {}

def test_graph_add_vertex():
    g = Graph()
    g.add_vertex("A")
    assert "A" in g.vertices

# def test_graph_add_duplicate_vertex():
#     g = Graph()
#     g.add_vertex("A")
#     with pytest.raises(KeyError):
#         g.add_vertex("A")

def test_graph_get_vertex():
    g = Graph()
    g.add_vertex("A")
    v = g.get_vertex("A")
    assert v.key == "A"

def test_graph_get_nonexistent_vertex():
    g = Graph()
    with pytest.raises(KeyError):
        g.get_vertex("B")

def test_vertex_in_graph():
    g = Graph()
    g.add_vertex("A")
    assert "A" in g

def test_vertex_not_in_graph():
    g = Graph()
    assert "B" not in g

# def test_add_edge():
#     g = Graph()
#     g.add_vertex("A")
#     g.add_vertex("B")
#     g.add_edge("A", "B", 5)
#     assert g.does_edge_exist("A", "B")
#     assert not g.does_edge_exist("B", "A")
#     assert g.get_vertex("A").get_neighbours() == {"B": 5}

def test_add_edge_to_nonexistent_vertex():
    g = Graph()
    g.add_vertex("A")
    with pytest.raises(KeyError):
        g.add_edge("A", "B", 10)

def test_vertex_add_neighbour():
    g = Graph()
    g.add_vertex("A")
    g.add_vertex("B")
    a = g.get_vertex("A")
    b = g.get_vertex("B")
    a.add_neighbour(b, 10)
    assert b in a.get_neighbours()

def test_vertex_does_it_point_to():
    g = Graph()
    g.add_vertex("A")
    g.add_vertex("B")
    a = g.get_vertex("A")
    b = g.get_vertex("B")
    a.add_neighbour(b, 10)
    assert a.does_it_point_to(b)

def test_dijkstra_basic():
    g = Graph()
    g.add_vertex("A")
    g.add_vertex("B")
    g.add_vertex("C")
    g.add_edge("A", "B", 1)
    g.add_edge("B", "C", 2)
    g.add_edge("A", "C", 4)
    distances = dijkstra(g, g.get_vertex("A"))
    assert distances[g.get_vertex("B")] == 1
    assert distances[g.get_vertex("C")] == 3

def test_dijkstra_unreachable_vertex():
    g = Graph()
    g.add_vertex("A")
    g.add_vertex("B")
    distances = dijkstra(g, g.get_vertex("A"))
    assert distances[g.get_vertex("B")] == float('inf')

# def test_dijkstra_empty_graph():
#     g = Graph()
#     with pytest.raises(ValueError):
#         dijkstra(g, g.get_vertex("A"))

# def test_dijkstra_nonexistent_source():
#     g = Graph()
#     g.add_vertex("A")
#     with pytest.raises(KeyError):
#         dijkstra(g, "B")

# def test_dijkstra_source_not_in_graph():
#     g = Graph()
#     g.add_vertex("A")
#     out_of_graph = Vertex("B")
#     with pytest.raises(KeyError):
#         dijkstra(g, out_of_graph)

def test_edge_default_weight():
    g = Graph()
    g.add_vertex("A")
    g.add_vertex("B")
    g.add_edge("A", "B")
    assert g.get_vertex("A").get_weight(g.get_vertex("B")) == 1



def test_dijkstra_tight_edge_condition():
    g = Graph()
    g.add_vertex("A")
    g.add_vertex("B")
    g.add_vertex("C")
    g.add_edge("A", "B", 5)
    g.add_edge("B", "C", 5)
    g.add_edge("A", "C", 10)
    distances = dijkstra(g, g.get_vertex("A"))
    assert distances[g.get_vertex("C")] == 10

