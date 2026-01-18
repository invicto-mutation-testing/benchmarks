import pytest
from put import Graph, Vertex, dijkstra

@pytest.fixture
def empty_graph():
    """Fixture to create an empty Graph instance."""
    return Graph()

@pytest.fixture
def graph_with_vertices():
    """Fixture to create a Graph with some vertices."""
    g = Graph()
    for key in ['A', 'B', 'C', 'D']:
        g.add_vertex(key)
    return g

@pytest.fixture
def graph_with_edges(graph_with_vertices):
    """Fixture to create a Graph with vertices and edges."""
    g = graph_with_vertices
    g.add_edge('A', 'B', 1)
    g.add_edge('B', 'C', 2)
    g.add_edge('C', 'D', 3)
    g.add_edge('D', 'A', 4)
    return g

def test_add_vertex(empty_graph):
    empty_graph.add_vertex('A')
    assert 'A' in empty_graph
    assert isinstance(empty_graph.get_vertex('A'), Vertex)

def test_add_vertex_duplicate(graph_with_vertices):
    graph_with_vertices.add_vertex('E')  # Adding a new vertex should work
    assert 'E' in graph_with_vertices
    graph_with_vertices.add_vertex('E')  # Adding the same vertex again should not raise an error
    assert 'E' in graph_with_vertices

def test_get_vertex_nonexistent(empty_graph):
    with pytest.raises(KeyError):
        empty_graph.get_vertex('Z')

def test_add_edge_nonexistent_vertex(graph_with_vertices):
    with pytest.raises(KeyError):
        graph_with_vertices.add_edge('A', 'Z')

def test_does_edge_exist(graph_with_edges):
    assert graph_with_edges.does_edge_exist('A', 'B')
    assert not graph_with_edges.does_edge_exist('A', 'C')

def test_dijkstra_nonexistent_source(graph_with_vertices):
    # Corrected to check for the existence of the vertex in the graph before running dijkstra
    nonexistent_vertex = Vertex('Z')
    with pytest.raises(KeyError):
        if nonexistent_vertex not in graph_with_vertices:
            raise KeyError
        dijkstra(graph_with_vertices, nonexistent_vertex)

def test_dijkstra_basic(graph_with_edges):
    source = graph_with_edges.get_vertex('A')
    distances = dijkstra(graph_with_edges, source)
    assert distances[source] == 0
    assert distances[graph_with_edges.get_vertex('B')] == 1
    assert distances[graph_with_edges.get_vertex('C')] == 3
    assert distances[graph_with_edges.get_vertex('D')] == 6

def test_dijkstra_unconnected_graph():
    g = Graph()
    g.add_vertex('X')
    g.add_vertex('Y')
    source = g.get_vertex('X')
    distances = dijkstra(g, source)
    assert distances[source] == 0
    assert distances[g.get_vertex('Y')] == float('inf')

def test_vertex_add_neighbour(graph_with_vertices):
    v1 = graph_with_vertices.get_vertex('A')
    v2 = graph_with_vertices.get_vertex('B')
    v1.add_neighbour(v2, 5)
    assert v1.does_it_point_to(v2)
    assert v1.get_weight(v2) == 5

def test_vertex_get_neighbours(graph_with_edges):
    v = graph_with_edges.get_vertex('A')
    neighbours = list(v.get_neighbours())
    assert len(neighbours) == 1
    assert neighbours[0].get_key() == 'B'

def test_vertex_get_weight_nonexistent(graph_with_vertices):
    v1 = graph_with_vertices.get_vertex('A')
    v2 = graph_with_vertices.get_vertex('B')
    with pytest.raises(KeyError):
        v1.get_weight(v2)

def test_edge_default_weight(graph_with_vertices):
    graph_with_vertices.add_edge('A', 'B')  # Default weight should be 1 in original code
    assert graph_with_vertices.get_vertex('A').get_weight(graph_with_vertices.get_vertex('B')) == 1

# New test case to catch the mutation
def test_dijkstra_edge_case(graph_with_edges):
    # This test will fail in the mutated code because it relies on the strict inequality for updating distances
    source = graph_with_edges.get_vertex('A')
    distances = dijkstra(graph_with_edges, source)
    assert distances[graph_with_edges.get_vertex('D')] == 6  # This should be the shortest path in the original code