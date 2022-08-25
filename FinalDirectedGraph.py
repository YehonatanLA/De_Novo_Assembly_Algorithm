from Graph import *
from Utilities import compare_prefix_suffix


# graph G star star

class FinalDirectedGraph(Graph):

    def __init__(self, induced_graph, original_string):
        Graph.__init__(self)
        self.induced_graph = induced_graph
        self.is_success = False
        # First part - Combine the vertices of I to single vertex
        roots = self.get_roots()
        self.num_of_vertices = len(roots)

        if roots:
            max_overlap_len = len(roots[0])
        else:
            # a very rare case
            print("ERROR---CYCLIC")
            exit(1)

        for root in roots:
            # change the old
            path_to_vertex = self.compress_path(root)
            self.add_vertex_with_no_edges(path_to_vertex)

        for vertex in self.dict_graph.keys():
            self.add_edges(vertex, max_overlap_len)

        self.for_one_vertex_case(original_string)

    # TODO: second step
    # def get_solution(self):
    #     return self.solution

    def for_one_vertex_case(self, original_string):
        if self.get_number_of_vertices() == 1 and original_string in self.dict_graph:
            self.is_success = True
        else:
            self.is_success = False

    def get_roots(self):
        roots = {vertex: True for vertex in self.induced_graph.dict_graph.keys()}
        for vertex, list_of_edges in self.induced_graph.dict_graph.items():
            for edge in list_of_edges:
                roots[edge.next_vertex] = False
        return [vertex for vertex, status in roots.items() if status]

    def compress_path(self, root):
        index = 0

        new_vertex = root

        [edge] = self.induced_graph.dict_graph[root]
        vertex = edge.next_vertex

        while vertex in self.induced_graph.dict_graph:
            join_tuple = (new_vertex, edge.next_vertex[edge.weight:])
            new_vertex = "".join(join_tuple)

            [edge] = self.induced_graph.dict_graph[vertex]
            vertex = edge.next_vertex

            index += 1
            if index > self.induced_graph.get_number_of_vertices():
                # a very rare case
                print("ERROR---CYCLIC")
                return ""

        join_tuple = (new_vertex, edge.next_vertex[edge.weight:])
        new_vertex = "".join(join_tuple)
        return new_vertex

    def add_edges(self, suffix_vertex, max_overlap_len):
        """
        :param max_overlap_len:
        :param suffix_vertex: the vertex to add edges from
        """
        for prefix_vertex in self.dict_graph.keys():
            if id(prefix_vertex) == id(suffix_vertex):
                continue
            for overlap_len in range(max_overlap_len - 1, 0, -1):
                if compare_prefix_suffix(overlap_len, prefix_vertex, suffix_vertex):
                    edge = Edge(overlap_len, prefix_vertex)
                    self.add_edge(suffix_vertex, edge)

    # def create_guess(self):
    #     """
    #     The function will use G** to create a guess of reconstructed string
    #     :return: the guess if there is one, empty string otherwise
    #     """
    #
    #     if self.num_of_vertices == 1:
    #         return self.dict_graph.keys()[0]
    #
    #     # all_edges_list will be a list that each item of index i is a list of all edges coming out of vertex i
    #     all_edges_list = [self.dict_graph[vertex] for vertex in self.dict_graph.keys()]
    #     guess = ""
