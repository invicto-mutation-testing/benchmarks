import pytest
from put import Graph, Vertex, dijkstra

# Fixtures for consistent and isolated test environment:
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
def complex_graph(graph_with_vertices):
    g = graph_with_vertices
    g.add_edge('A', 'B', 1)
    g.add_edge('A', 'C', 4)
    g.add_edge('B', 'C', 2)
    g.add_edge('C', 'D', 1)
    return g

# Test cases for Vertex
def test_vertex_initialization():
    vertex = Vertex("A")
    assert vertex.key == "A"
    assert vertex.points_to == {}

def test_vertex_add_neighbour():
    v1 = Vertex("A")
    v2 = Vertex("B")
    v1.add_neighbour(v2, 5)
    assert v1.points_to[v2] == 5

def test_vertex_neighbours():
    v1 = Vertex("A")
    v2 = Vertex("B")
    v3 = Vertex("C")
    v1.add_neighbour(v2, 5)
    v1.add_neighbour(v3, 10)
    assert set(v1.get_neighbours()) == {v2, v3}

# Test cases for Graph
def test_empty_graph_initialization(empty_graph):
    assert isinstance(empty_graph.vertices, dict)
    assert len(empty_graph.vertices) == 0

def test_add_vertex(graph_with_vertices):
    graph_with_vertices.add_vertex("E")
    assert "E" in graph_with_vertices.vertices

def test_get_vertex(graph_with_vertices):
    key = 'A'
    assert graph_with_vertices.get_vertex(key).key == key

def test_graph_contains(graph_with_vertices):
    assert 'A' in graph_with_vertices

def test_add_edge(graph_with_vertices):
    graph_with_vertices.add_edge('A', 'B', 2)
    assert graph_with_vertices.does_edge_exist('A', 'B')

def test_does_edge_exist(complex_graph):
    assert complex_graph.does_edge_exist('A', 'C') == True
    assert complex_graph.does_edge_exist('C', 'A') == False

# Test Dijkstra's Algorithm
def test_dijkstra_initial_distance(complex_graph):
    source = complex_graph.get_vertex('A')
    distances = dijkstra(complex_graph, source)
    assert distances[source] == 0

def test_dijkstra_calculation(complex_graph):
    source = complex_graph.get_vertex('A')
    distances = dijkstra(complex_graph, source)
    assert distances[complex_graph.get_vertex('D')] == 4  # A to C to D = 4

# Exception handling test cases
@pytest.mark.xfail(reason="Adding existing vertex does not raise an exception")
def test_add_vertex_exception(graph_with_vertices):
    graph_with_vertices.add_vertex("A")  # Assuming the code allows duplicate additions quietly

def test_get_vertex_exception(empty_graph):
    with pytest.raises(KeyError):
        empty_graph.get_vertex("A")  # Not existent vertex

def test_add_edge_exception_no_src(graph_with_vertices):
    with pytest.raises(KeyError):
        graph_with_vertices.add_edge("E", "A")  # "E" not added yet

def test_add_edge_exception_no_dest(graph_with_vertices):
    with pytest.raises(KeyError):
        graph_with_vertices.add_edge("A", "E")  # "E" not added yet

@pytest.mark.xfail(reason="Dijkstra does not raise KeyError on non-existent vertex in graph")
def test_dijkstra_nonexistent_source(complex_graph):
    bogus_vertex = Vertex("Z")
    dijkstra(complex_graph, bogus_vertex)  # Assuming Dijkstra quietly fails

# New test to catch mutation in edge weight default
def test_default_edge_weight_mutant(graph_with_vertices):
    graph_with_vertices.add_vertex("E")
    graph_with_vertices.add_edge('A', 'E')  # Default weight should be 1
    # In the original code, the assumption is that default weight is 1
    # Mutated code changes this to 2, so this test should fail against mutated while pass against original
    assert graph_with_vertices.get_vertex('A').get_weight(graph_with_vertices.get_vertex('E')) == 1

def test_mutation_on_compare_operator_dijkstra(graph_with_vertices):
    graph_with_vertices.add_edge('A', 'B', 5)
    graph_with_vertices.add_edge('A', 'C', 2)
    graph_with_vertices.add_edge('C', 'B', 1)
    source = graph_with_vertices.get_vertex('A')
    distance = dijkstra(graph_with_vertices, source)
    # The change in mutation affects whether we update a distance or not:
    assert distance[graph_with_vertices.get_vertex('B')] == 3  # A->C->B, expecting 3 not 5 (mutated may give 5 if not catching equal weights)