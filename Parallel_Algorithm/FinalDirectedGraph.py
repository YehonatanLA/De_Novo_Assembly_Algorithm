from Parallel_Algorithm.Graph import *
from Parallel_Algorithm.Utilities import compare_prefix_suffix


# graph G star star

class FinalDirectedGraph(Graph):

    def __init__(self, induced_graph):
        Graph.__init__(self)
        self.induced_graph = induced_graph
        # self.is_success = False
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

    def get_roots(self):
        roots = {vertex: True for vertex in self.induced_graph.dict_graph.keys()}
        for vertex, list_of_edges in self.induced_graph.dict_graph.items():
            for edge in list_of_edges:
                roots[edge.next_vertex] = False
        return [vertex for vertex, status in roots.items() if status]

    def compress_path(self, root):
        index = 0
        new_vertex = root
        vertex = root

        while self.induced_graph.dict_graph[vertex]:
            [edge] = self.induced_graph.dict_graph[vertex]
            join_tuple = (new_vertex, edge.next_vertex[edge.weight:])
            new_vertex = "".join(join_tuple)

            vertex = edge.next_vertex

            index += 1
            if index > self.induced_graph.get_number_of_vertices():
                # a very rare case

                print("ERROR---CYCLIC")
                return ""

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
