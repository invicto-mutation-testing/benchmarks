class Graph:
    def __init__(self):
        
        self.vertices = {}

    def add_vertex(self, key):
        
        vertex = Vertex(key)
        self.vertices[key] = vertex

    def get_vertex(self, key):
        
        return self.vertices[key]

    def __contains__(self, key):
        return key in self.vertices

    def add_edge(self, src_key, dest_key, weight=1):
        
        self.vertices[src_key].add_neighbour(self.vertices[dest_key], weight)

    def does_edge_exist(self, src_key, dest_key):
        
        return self.vertices[src_key].does_it_point_to(self.vertices[dest_key])

    def __iter__(self):
        return iter(self.vertices.values())


class Vertex:
    def __init__(self, key):
        self.key = key
        self.points_to = {}

    def get_key(self):
        
        return self.key

    def add_neighbour(self, dest, weight):
        
        self.points_to[dest] = weight

    def get_neighbours(self):
        
        return self.points_to.keys()

    def get_weight(self, dest):
        
        return self.points_to[dest]

    def does_it_point_to(self, dest):
        
        return dest in self.points_to


def dijkstra(g, source):
    
    unvisited = set(g)
    distance = dict.fromkeys(g, float('inf'))
    distance[source] = 0

    while unvisited != set():
        
        closest = min(unvisited, key=lambda v: distance[v])

        
        unvisited.remove(closest)

        
        for neighbour in closest.get_neighbours():
            if neighbour in unvisited:
                new_distance = distance[closest] + closest.get_weight(neighbour)
                if distance[neighbour] > new_distance:
                    distance[neighbour] = new_distance

    return distance

