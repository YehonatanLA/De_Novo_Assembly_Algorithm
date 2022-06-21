from Graph import Graph


# graph G star star
class FinalDirectedGraph(Graph):

    def __init__(self, induced_graph):
        Graph.__init__(self)
        self.induced_graph = induced_graph

        # ---------------------------------------
        self.solution = ""  # for testing
        # ---------------------------------------
        roots = self.get_roots()

        # first step for building the final directed graph
        for root in roots:
            new_vertex = self.get_new_vertex_from_root(root)
            self.dict_graph[new_vertex] = []

        if len(self.dict_graph.keys()) == 1:
            [self.solution] = self.dict_graph.keys()

        # second step for building the final directed graph
        # TODO: second step

    def get_solution(self):
        return self.solution

    def get_roots(self):
        roots = {vertex: True for vertex in self.induced_graph.dict_graph.keys()}
        for vertex, list_of_edges in self.induced_graph.dict_graph.items():
            for edge in list_of_edges:
                roots[edge.next_vertex] = False
        return [vertex for vertex, status in roots.items() if status]

    def get_new_vertex_from_root(self, root):
        new_vertex = root
        list_of_edges = self.induced_graph.dict_graph[root]

        if not list_of_edges:
            return root

        [edge] = list_of_edges  # we assume that there is only one element

        while edge.next_vertex in self.induced_graph.dict_graph.keys():
            new_vertex += edge.next_vertex[edge.weight:]
            [edge] = self.induced_graph.dict_graph[edge.next_vertex]

        new_vertex += edge.next_vertex[edge.weight:]
        return new_vertex
