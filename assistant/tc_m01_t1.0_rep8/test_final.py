import pytest
from put import Graph, Vertex, dijkstra

class TestGraph:
    @pytest.fixture
    def graph(self):
        g = Graph()
        for key in ['A', 'B', 'C', 'D']:
            g.add_vertex(key)
        return g

    def test_add_vertex(self, graph):
        graph.add_vertex('E')
        assert 'E' in graph

    def test_add_vertex_duplicate_key(self, graph):
        graph.add_vertex('A')
        assert 'A' in graph

    def test_get_vertex(self, graph):
        vertex = graph.get_vertex('A')
        assert isinstance(vertex, Vertex)
        assert vertex.get_key() == 'A'

    def test_get_vertex_nonexistent(self, graph):
        with pytest.raises(KeyError):
            graph.get_vertex('Nonexistent')

    def test_add_edge(self, graph):
        graph.add_edge('A', 'B', 5)
        assert graph.does_edge_exist('A', 'B')

    def test_add_edge_nonexistent_vertex(self, graph):
        with pytest.raises(KeyError):
            graph.add_edge('A', 'Z', 1)

    def test_iter(self, graph):
        vertex_keys = {vertex.get_key() for vertex in graph}
        assert vertex_keys == {'A', 'B', 'C', 'D'}

class TestDijkstra:
    @pytest.fixture
    def setup_graph(self):
        g = Graph()
        vertices = ['A', 'B', 'C']
        for v in vertices:
            g.add_vertex(v)
        g.add_edge('A', 'B', 1)
        g.add_edge('A', 'C', 5)
        return g, g.get_vertex('A')

    def test_dijkstra(self, setup_graph):
        g, source = setup_graph
        distances = dijkstra(g, source)
        assert distances == {g.get_vertex('A'): 0, g.get_vertex('B'): 1, g.get_vertex('C'): 5}

    def test_dijkstra_unconnected_graph(self, setup_graph):
        g, source = setup_graph
        g.add_vertex('D')
        distances = dijkstra(g, source)
        assert distances[g.get_vertex('D')] == float('inf')

    def test_dijkstra_nonexistent_source(self, setup_graph):
        g, _ = setup_graph
        non_existing_vertex = Vertex('Z')
        g.add_vertex('Z')
        distances = dijkstra(g, non_existing_vertex)
        assert distances[non_existing_vertex] == 0

    # New test cases to catch mutation
    def test_dijkstra_exact_distances_check(self, setup_graph):
        g, source = setup_graph
        g.add_edge('B', 'C', 4)  # A to C direct is 5, A to C via B is 1+4=5
        distances = dijkstra(g, source)
        expected_distances = {
            g.get_vertex('A'): 0,
            g.get_vertex('B'): 1,
            g.get_vertex('C'): 5  # Confirming that 5 is chosen over any other like 5 via an alternative path
        }
        assert distances == expected_distances