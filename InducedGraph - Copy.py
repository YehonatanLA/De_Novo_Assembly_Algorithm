from Graph import *
from Utilities import is_real_overlap

# graph I

class InducedGraph(Graph):

    def __init__(self, all_overlap_graph, real_read_len):
        Graph.__init__(self)
        self.all_overlap_graph = all_overlap_graph
        self.num_of_vertices = self.all_overlap_graph.num_of_vertices

        for vertex in self.all_overlap_graph.dict_graph.keys():
            max_edge = self.get_max_edge(vertex, real_read_len)
            if max_edge is not None:
                self.dict_graph[vertex] = max_edge

    def get_max_edge(self, vertex, real_read_len):
        overlap_lists = self.all_overlap_graph.dict_graph[vertex]
        prefix_matches = 0

        for list_index in range(len(vertex) - 1, real_read_len - 1, -1):
            if not overlap_lists[list_index]:
                continue

            for read in overlap_lists[list_index]:
                if is_real_overlap(vertex, read, list_index) and vertex is read:
                    prefix_matches += 1

            if prefix_matches == 1:
                overlap = len(vertex) - list_index
                return Edge(list_index, vertex[overlap:], overlap_lists[list_index][0])
            else:
                return None
