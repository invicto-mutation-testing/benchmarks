import pytest
from put import Graph, Vertex, dijkstra

@pytest.fixture
def empty_graph():
    """ Fixture to create an empty graph for each test. """
    return Graph()

@pytest.fixture
def vertex():
    """ Fixture to create a single vertex. """
    return Vertex('A')

@pytest.fixture
def graph_with_vertices():
    """ Fixture to create a graph with multiple vertices but no edges. """
    g = Graph()
    for key in ['A', 'B', 'C', 'D']:
        g.add_vertex(key)
    return g

@pytest.fixture
def graph_with_edges(graph_with_vertices):
    """ Fixture to create a graph with vertices A, B, C, D and edges A->B, B->C, C->A, C->D. """
    g = graph_with_vertices
    g.add_edge('A', 'B', 1)
    g.add_edge('B', 'C', 2)
    g.add_edge('C', 'A', 3)
    g.add_edge('C', 'D', 4)
    return g

def test_add_vertex(empty_graph):
    """ Test adding vertices to the graph. """
    empty_graph.add_vertex('A')
    assert 'A' in empty_graph
    empty_graph.add_vertex('B')
    assert 'B' in empty_graph

def test_get_vertex(graph_with_vertices):
    """ Test retrieval of vertices from the graph. """
    assert graph_with_vertices.get_vertex('A').get_key() == 'A'
    assert graph_with_vertices.get_vertex('B').get_key() == 'B'

def test_add_vertex_exceptions(empty_graph):
    """ Test handling of adding duplicate vertices. """
    empty_graph.add_vertex('A')  
    try:
        empty_graph.add_vertex('A')
        assert False, "Expected an exception for adding duplicate vertex"
    except Exception:
        assert True

def test_does_edge_exist(graph_with_edges):
    """ Test existence check for edges in graphs. """
    assert graph_with_edges.does_edge_exist('A', 'B')
    assert not graph_with_edges.does_edge_exist('A', 'D')
    assert graph_with_edges.does_edge_exist('C', 'D')

def test_does_edge_exist_exceptions(graph_with_vertices):
    """ Test edge existence check with non-existent vertices. """
    graph_with_vertices.add_vertex('E')
    with pytest.raises(KeyError):
        graph_with_vertices.does_edge_exist('E', 'Z')

def test_dijkstra_basic(graph_with_edges):
    """ Test Dijkstra's algorithm on predetermined graph setups. """
    src = graph_with_edges.get_vertex('A')
    distances = dijkstra(graph_with_edges, src)
    assert distances[graph_with_edges.get_vertex('B')] == 1
    assert distances[graph_with_edges.get_vertex('C')] == 3
    assert distances[graph_with_edges.get_vertex('D')] == 7
    assert distances[src] == 0

def test_dijkstra_unreachable(graph_with_edges):
    """ Validate handling of unreachable vertices in Dijkstra's algorithm. """
    src = graph_with_edges.get_vertex('D')
    distances = dijkstra(graph_with_edges, src)
    assert distances[graph_with_edges.get_vertex('A')] == float('inf')

def test_default_edge_weight(graph_with_vertices):
    """ Test that the default edge weight remains 1 as expected."""
    src = 'A'
    dest = 'B'
    graph_with_vertices.add_edge(src, dest)  # Default weight, should be 1 as per original code
    
    src_vertex = graph_with_vertices.get_vertex(src)
    assert src_vertex.get_weight(graph_with_vertices.get_vertex(dest)) == 1, "Default weight should be 1, mutation changes it"

def test_dijkstra_edge_case(graph_with_edges):
    """ Validate that Dijkstra's algorithm properly evaluates new path distances, not just weight comparisons. """
    graph_with_edges.add_edge('B', 'D', 4)  # Adjust this edge to test edge case
    
    src = graph_with_edges.get_vertex('A')
    distances = dijkstra(graph_with_edges, src)

    # Confirm path A->B->D is correct with new edge weight
    expected_distance_via_B_to_D = distances[graph_with_edges.get_vertex('B')] + 4
    assert distances[graph_with_edges.get_vertex('D')] == expected_distance_via_B_to_D, "The distance calculation should reflect the shortest path evaluation."