from Graph import *
from Utilities import compare_prefix_suffix

# graph G star star

class FinalDirectedGraph(Graph):

    def __init__(self, induced_graph):
        Graph.__init__(self)
        self.induced_graph = induced_graph
        # First part - Combine the vertices of I to single vertex
        roots = self.get_roots()
        self.num_of_vertices = len(roots)
        max_overlap_len = len(roots[0])

        for root in roots:
            # change the old
            path_to_vertex = self.compress_path(root, induced_graph)
            self.dict_graph[path_to_vertex] = []

        for vertex in self.dict_graph.keys():
            self.add_edges(vertex, max_overlap_len)

    # # ---------------------------------------
    # self.solution = ""  # for testing
    # # ---------------------------------------
    #
    # # first step for building the final directed graph
    # for root in roots:
    #     new_vertex = self.get_new_vertex_from_root(root)
    #     self.dict_graph[new_vertex] = []
    #
    # if len(self.dict_graph.keys()) == 1:
    #     [self.solution] = self.dict_graph.keys()

    # second step for building the final directed graph
    # TODO: second step

    # def get_solution(self):
    #     return self.solution

    def get_roots(self):
        roots = {vertex: True for vertex in self.induced_graph.dict_graph.keys()}
        for vertex, list_of_edges in self.induced_graph.dict_graph.items():
            for edge in list_of_edges:
                roots[edge.next_vertex] = False
        return [vertex for vertex, status in roots.items() if status]

    def compress_path(self, root, induced_graph):
        """
        :param root: the vertex which holds the path that will be compressed
        :param induced_graph: the induced graph with some
        :return: the compressed vertex
        """
        """
        Way this function operates: for each vertex in path, we put in the string from index 0 until overlap starts
        """
        vertex_length = len(root)
        inner_edge = induced_graph[root]
        new_vertex = ""
        curr_vertex = root

        while inner_edge is not None:
            join_tuple = (new_vertex, curr_vertex[:vertex_length - inner_edge.weight])
            new_vertex = "".join(join_tuple)
            curr_vertex = inner_edge.next_vertex
            inner_edge = induced_graph[curr_vertex]
        """
        Need to add the final vertex from path to string, since it doesn't have an edge
        """
        new_vertex = "".join((new_vertex, curr_vertex))
        return new_vertex

    def add_edges(self, suffix_vertex, max_overlap_len):
        """
        :param suffix_vertex: the vertex to add edges from
        :return: nothing
        """
        edges_list = []
        # TODO: doing this the naive way, if there is a better than optimize here
        for prefix_vertex in self.dict_graph.keys():

            for overlap_len in range(max_overlap_len - 1, 0, -1):
                if compare_prefix_suffix(overlap_len, prefix_vertex, suffix_vertex):
                    edges_list.append(Edge(overlap_len, prefix_vertex))
                    # break
        self.dict_graph[suffix_vertex] = edges_list

    def create_guess(self):
        """
        The function will use G** to create a guess of reconstructed string
        :return: the guess if there is one, empty string otherwise
        """

        if self.num_of_vertices == 1:
            return self.dict_graph.keys()[0]

        # all_edges_list will be a list that each item of index i is a list of all edges coming out of vertex i
        all_edges_list = [self.dict_graph[vertex] for vertex in self.dict_graph.keys()]
        guess = ""
