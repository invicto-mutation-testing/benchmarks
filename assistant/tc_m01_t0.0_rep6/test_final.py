import pytest
from put import Graph, Vertex, dijkstra

@pytest.fixture
def empty_graph():
    return Graph()

@pytest.fixture
def graph_with_vertices():
    g = Graph()
    for key in ['A', 'B', 'C', 'D']:
        g.add_vertex(key)
    return g

@pytest.fixture
def graph_with_edges(graph_with_vertices):
    g = graph_with_vertices
    g.add_edge('A', 'B', 1)
    g.add_edge('A', 'C', 3)
    g.add_edge('B', 'C', 1)
    g.add_edge('C', 'D', 2)
    g.add_edge('D', 'A', 4)
    return g

def test_add_vertex(empty_graph):
    empty_graph.add_vertex('A')
    assert 'A' in empty_graph
    assert isinstance(empty_graph.get_vertex('A'), Vertex)

def test_add_edge(graph_with_vertices):
    graph_with_vertices.add_edge('A', 'B', 2)
    assert graph_with_vertices.does_edge_exist('A', 'B')

def test_dijkstra_basic(graph_with_edges):
    source = graph_with_edges.get_vertex('A')
    distances = dijkstra(graph_with_edges, source)
    expected_distances = {'A': 0, 'B': 1, 'C': 2, 'D': 4}
    actual_distances = {vertex.get_key(): distances[vertex] for vertex in distances}
    assert actual_distances == expected_distances

def test_dijkstra_unreachable(graph_with_vertices):
    graph_with_vertices.add_edge('A', 'B', 1)
    source = graph_with_vertices.get_vertex('A')
    distances = dijkstra(graph_with_vertices, source)
    assert distances[graph_with_vertices.get_vertex('C')] == float('inf')

def test_vertex_not_in_graph(empty_graph):
    with pytest.raises(KeyError):
        empty_graph.get_vertex('Z')

def test_edge_not_in_graph(graph_with_vertices):
    with pytest.raises(KeyError):
        graph_with_vertices.add_edge('A', 'Z', 1)

def test_default_edge_weight(graph_with_vertices):
    graph_with_vertices.add_edge('A', 'B')  # No weight specified, should use default weight
    assert graph_with_vertices.get_vertex('A').get_weight(graph_with_vertices.get_vertex('B')) == 1

def test_edge_weight_specified(graph_with_vertices):
    graph_with_vertices.add_edge('A', 'B', 3)  # Weight specified explicitly
    assert graph_with_vertices.get_vertex('A').get_weight(graph_with_vertices.get_vertex('B')) == 3

def test_dijkstra_with_default_weight(graph_with_vertices):
    graph_with_vertices.add_edge('A', 'B')
    graph_with_vertices.add_edge('B', 'C')
    source = graph_with_vertices.get_vertex('A')
    distances = dijkstra(graph_with_vertices, source)
    expected_distances = {'A': 0, 'B': 1, 'C': 2}  # Expecting default weights of 1
    actual_distances = {vertex.get_key(): distances[vertex] for vertex in distances if vertex.get_key() in expected_distances}
    assert actual_distances == expected_distances

# New test case to catch the mutation
def test_dijkstra_edge_case(graph_with_edges):
    # Adding an edge with the same weight as an existing shortest path to test the mutation
    graph_with_edges.add_edge('C', 'B', 1)  # This creates a cycle with equal weights
    source = graph_with_edges.get_vertex('A')
    distances = dijkstra(graph_with_edges, source)
    expected_distances = {'A': 0, 'B': 1, 'C': 2, 'D': 4}
    actual_distances = {vertex.get_key(): distances[vertex] for vertex in distances}
    assert actual_distances == expected_distances  # This should pass in original and fail in mutant where `>=` allows unnecessary updates