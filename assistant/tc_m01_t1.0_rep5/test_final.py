import pytest
from put import Graph, Vertex, dijkstra

# Fixture to create a clean graph for each test
@pytest.fixture
def graph():
    return Graph()

# Fixture to create vertices
@pytest.fixture
def vertices():
    return Vertex('A'), Vertex('B'), Vertex('C'), Vertex('D')

def test_add_vertex(graph):
    graph.add_vertex('A')
    assert 'A' in graph
    assert isinstance(graph.get_vertex('A'), Vertex)

def test_add_vertex_duplicate(graph):
    graph.add_vertex('A')
    graph.add_vertex('A')
    assert 'A' in graph

def test_get_vertex_missing(graph):
    with pytest.raises(KeyError):
        graph.get_vertex('Z')

def test_add_edge(graph, vertices):
    v1, v2, _, _ = vertices
    graph.vertices[v1.key] = v1
    graph.vertices[v2.key] = v2
    graph.add_edge(v1.key, v2.key)
    assert graph.does_edge_exist(v1.key, v2.key)

def test_add_edge_nonexistent_vertices(graph):
    with pytest.raises(KeyError):
        graph.add_edge('X', 'Y')

def test_vertex_add_neighbour_self(vertices):
    v1, _, _, _ = vertices
    v1.add_neighbour(v1, 5)
    assert v1.does_it_point_to(v1)

def test_vertex_nonexistent_neighbour_weight(graph, vertices):
    v1, v2, _, _ = vertices
    graph.vertices[v1.key] = v1
    graph.vertices[v2.key] = v2
    v1.add_neighbour(v2, 3)
    with pytest.raises(KeyError):
        _ = v1.get_weight(Vertex('Z'))

def test_iter_graph(graph, vertices):
    for v in vertices:
        graph.add_vertex(v.key)
    assert set([vertex.key for vertex in graph]) == set([v.key for v in vertices])

def test_add_edge_default_weight(graph, vertices):
    v1, v2, _, _ = vertices
    graph.vertices[v1.key] = v1
    graph.vertices[v2.key] = v2
    graph.add_edge(v1.key, v2.key)
    assert v1.get_weight(v2) == 1, "Default weight should be 1, found mutant with different weight"

def test_dijkstra_check_edge_weights(graph, vertices):
    v1, v2, v3, v4 = vertices
    graph.vertices[v1.key] = v1
    graph.vertices[v2.key] = v2
    graph.vertices[v3.key] = v3
    graph.vertices[v4.key] = v4
    graph.add_edge(v1.key, v2.key)
    graph.add_edge(v2.key, v3.key)
    graph.add_edge(v3.key, v4.key)
    assert v1.get_weight(v2) == 1, "Edge weight from A to B should be 1"
    assert v2.get_weight(v3) == 1, "Edge weight from B to C should be 1"
    assert v3.get_weight(v4) == 1, "Edge weight from C to D should be 1"

def test_dijkstra_basic(graph, vertices):
    v1, v2, v3, _ = vertices
    graph.vertices[v1.key] = v1
    graph.vertices[v2.key] = v2
    graph.vertices[v3.key] = v3
    graph.add_edge(v1.key, v2.key, 1)
    graph.add_edge(v2.key, v3.key, 2)
    distances = dijkstra(graph, v1)
    assert distances[v2] == 1, "Distance from A to B should be 1"
    assert distances[v3] == 3, "Distance from A to C should be 3"

def test_dijkstra_unconnected_vertex(graph, vertices):
    v1, v2, v3, v4 = vertices
    graph.vertices[v1.key] = v1
    graph.vertices[v2.key] = v2
    graph.vertices[v3.key] = v3
    graph.vertices[v4.key] = v4
    graph.add_edge(v1.key, v2.key, 1)
    distances = dijkstra(graph, v1)
    assert distances[v4] == float('inf'), "Unconnected vertex D should have infinite distance from A"

def test_dijkstra_no_vertices(graph):
    v = Vertex('Z')
    graph.vertices['Z'] = v
    distances = dijkstra(graph, v)
    assert distances[v] == 0, "Distance from vertex Z to itself should be 0"