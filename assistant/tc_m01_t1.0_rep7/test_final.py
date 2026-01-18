import pytest
from put import Graph, Vertex, dijkstra

class TestGraph:
    @pytest.fixture
    def graph(self):
        """Fixture to create a new graph for each test case."""
        return Graph()

    @pytest.fixture
    def vertex_keys(self):
        """Fixture to provide vertex keys."""
        return ['A', 'B', 'C', 'D', 'E']

    @pytest.fixture
    def add_vertices(self, graph, vertex_keys):
        """Fixture to add several vertices to a graph."""
        for key in vertex_keys:
            graph.add_vertex(key)
        return graph

    def test_add_vertex(self, graph):
        graph.add_vertex('A')
        assert 'A' in graph
        assert isinstance(graph.get_vertex('A'), Vertex)

    def test_get_vertex_invalid_key(self, graph):
        with pytest.raises(KeyError):
            graph.get_vertex('Z')

    def test_vertex_in_graph(self, graph, add_vertices):
        assert 'A' in graph
        assert 'Z' not in graph

    def test_add_edge_and_check_existence(self, add_vertices):
        graph = add_vertices
        graph.add_edge('A', 'B')
        assert graph.does_edge_exist('A', 'B') is True
        assert graph.does_edge_exist('B', 'A') is False

    def test_add_edge_invalid_vertex(self, add_vertices):
        graph = add_vertices
        with pytest.raises(KeyError):
            graph.add_edge('Z', 'A')
        with pytest.raises(KeyError):
            graph.add_edge('A', 'Z')

    def test_dijkstra_basic(self, add_vertices):
        graph = add_vertices
        graph.add_edge('A', 'B', 1)
        graph.add_edge('B', 'C', 2)
        source = graph.get_vertex('A')
        result = dijkstra(graph, source)
        assert result[graph.get_vertex('B')] == 1
        assert result[graph.get_vertex('C')] == 3

    def test_dijkstra_no_path(self, add_vertices):
        graph = add_vertices
        graph.add_edge('A', 'B', 1)
        source = graph.get_vertex('A')
        dest = graph.get_vertex('C')
        result = dijkstra(graph, source)
        assert result[dest] == float('inf')

    def test_dijkstra_with_self_loop(self, add_vertices):
        graph = add_vertices
        graph.add_edge('A', 'A', 5)
        source = graph.get_vertex('A')
        result = dijkstra(graph, source)
        assert result[graph.get_vertex('A')] == 0

    def test_dijkstra_unconnected_graph(self, add_vertices):
        graph = add_vertices
        source = graph.get_vertex('A')
        result = dijkstra(graph, source)
        assert all(result[v] == float('inf') for v in graph if v != source)

    def test_default_weight_original(self, add_vertices):
        graph = add_vertices
        graph.add_edge('A', 'B')  # By default weight 1 should be used here
        assert graph.get_vertex('A').get_weight(graph.get_vertex('B')) == 1

    def test_modified_weight(self, add_vertices):
        graph = add_vertices
        graph.add_edge('A', 'C')
        assert graph.get_vertex('A').get_weight(graph.get_vertex('C')) == 1

    ### New Tests to catch the mutation

    def test_vertex_initialization_key(self, graph):
        vertex = Vertex('X')
        assert vertex.key == 'X', "Vertex key should remain as initialized, was mutated to None."

    def test_vertex_initialization_key_from_graph(self, graph):
        graph.add_vertex('Y')
        vertex = graph.get_vertex('Y')
        assert vertex.key == 'Y', "Vertex key should be 'Y', but was mutated."

    ### Additional test specifically targeting the mutation difference
    def test_dijkstra_tight_comparison(self, add_vertices):
        """ Test that the comparison does not allow for equal weight updates, as in original. """
        graph = add_vertices
        graph.add_edge('A', 'B', 1)
        graph.add_edge('B', 'A', 1)  # Back edge making the mutation relevant
        source = graph.get_vertex('A')
        dest = graph.get_vertex('B')
        dijkstra_result = dijkstra(graph, source)
        assert dijkstra_result[dest] == 1, "The path should update only if the new distance is strictly less in the original code."