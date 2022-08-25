class Graph:
    def __init__(self):
        self.dict_graph = {}
        self.vertices = set()

    def add_edge(self, vertx, edge):
        if vertx not in self.dict_graph:
            self.dict_graph[vertx] = []
        self.dict_graph[vertx].append(edge)

        self.vertices.add(vertx)
        self.vertices.add(edge.next_vertex)

    def add_vertex_with_no_edges(self, vertex):
        self.dict_graph[vertex] = []
        self.vertices.add(vertex)

    def get_number_of_vertices(self):
        return len(self.vertices)

    def print_graph(self, title):
        print(title)
        print(f"number of vertices: {self.get_number_of_vertices()}\n")
        for vertex, edges_lst in self.dict_graph.items():

            if len(self.dict_graph.items()) == 1:
                print(len(vertex))

            print(f"vertex: {vertex}")
            for edge in edges_lst:
                edge.print_edge()
            print("\n")


class Edge:
    def __init__(self, weight, next_vertex):
        self.weight = weight
        self.next_vertex = next_vertex

    def print_edge(self):
        print(f"next vertex: {self.next_vertex}, weight of edge: {self.weight}")
