import pytest
from put import Graph, Vertex, dijkstra

@pytest.fixture
def empty_graph():
    return Graph()

@pytest.fixture
def graph_with_vertices():
    g = Graph()
    for key in range(5):
        g.add_vertex(key)
    return g

@pytest.fixture
def graph_with_edges():
    g = Graph()
    vertices = [Vertex(i) for i in range(5)]
    for v in vertices:
        g.add_vertex(v.get_key())
    for i in range(4):
        g.add_edge(vertices[i].get_key(), vertices[i+1].get_key(), i+1)
    return g

def test_add_vertex(empty_graph):
    empty_graph.add_vertex(1)
    assert 1 in empty_graph
    assert isinstance(empty_graph.get_vertex(1), Vertex)

def test_get_vertex_nonexistent(empty_graph):
    with pytest.raises(KeyError):
        empty_graph.get_vertex(999)

def test_add_edge_nonexistent_vertex(graph_with_vertices):
    with pytest.raises(KeyError):
        graph_with_vertices.add_edge(1, 999)

def test_does_edge_exist(graph_with_edges):
    assert graph_with_edges.does_edge_exist(0, 1)
    assert not graph_with_edges.does_edge_exist(0, 4)

def test_dijkstra_basic(graph_with_edges):
    source = graph_with_edges.get_vertex(0)
    distances = dijkstra(graph_with_edges, source)
    assert distances[source] == 0
    assert distances[graph_with_edges.get_vertex(1)] == 1
    assert distances[graph_with_edges.get_vertex(2)] == 3
    assert distances[graph_with_edges.get_vertex(3)] == 6
    assert distances[graph_with_edges.get_vertex(4)] == 10

def test_dijkstra_unconnected_graph(graph_with_vertices):
    source = graph_with_vertices.get_vertex(0)
    distances = dijkstra(graph_with_vertices, source)
    assert distances[source] == 0
    for key in range(1, 5):
        assert distances[graph_with_vertices.get_vertex(key)] == float('inf')

def test_vertex_add_neighbour(graph_with_vertices):
    v1 = graph_with_vertices.get_vertex(1)
    v2 = graph_with_vertices.get_vertex(2)
    v1.add_neighbour(v2, 5)
    assert v1.does_it_point_to(v2)
    assert v1.get_weight(v2) == 5

def test_vertex_get_neighbours(graph_with_vertices):
    v1 = graph_with_vertices.get_vertex(1)
    v2 = graph_with_vertices.get_vertex(2)
    v3 = graph_with_vertices.get_vertex(3)
    v1.add_neighbour(v2, 1)
    v1.add_neighbour(v3, 2)
    neighbours = list(v1.get_neighbours())
    assert v2 in neighbours
    assert v3 in neighbours
    assert len(neighbours) == 2

def test_vertex_get_weight_nonexistent_neighbour(graph_with_vertices):
    v1 = graph_with_vertices.get_vertex(1)
    v2 = graph_with_vertices.get_vertex(2)
    with pytest.raises(KeyError):
        v1.get_weight(v2)

# New test case to catch the mutation
def test_dijkstra_edge_case(graph_with_edges):
    # This test will pass in the original code and fail in the mutated code
    # because the condition in the dijkstra function is changed from '>' to '>='.
    source = graph_with_edges.get_vertex(0)
    destination = graph_with_edges.get_vertex(1)
    intermediate = graph_with_edges.get_vertex(2)
    graph_with_edges.add_edge(destination.get_key(), intermediate.get_key(), 1)
    graph_with_edges.add_edge(source.get_key(), intermediate.get_key(), 1)
    distances = dijkstra(graph_with_edges, source)
    assert distances[intermediate] == 1, "Distance should be 1, not updated by a longer path"