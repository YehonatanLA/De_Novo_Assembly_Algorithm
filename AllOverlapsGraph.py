from Graph import *
from Utilities import *

# graph G star
def get_overlap(suffix_vertex, prefix_vertex):
    """
    :param suffix_vertex:
    :param prefix_vertex:
    :return: new edge base on the overlap of 2 vertices(2 strings)
    """

    i = suffix_vertex.find(prefix_vertex[0])
    while i >= 0:
        if prefix_vertex.startswith(suffix_vertex[i:]):
            final_overlap = suffix_vertex[i:]
            return Edge(len(final_overlap), final_overlap, prefix_vertex)

        i = suffix_vertex.find(prefix_vertex[0], i + 1)

    return None


class AllOverlapsGraph(Graph):

    def __init__(self, reads_lst):
        Graph.__init__(self)
        self.reads_lst = reads_lst
        self.add_vertices()

    def add_vertices(self):
        # first insert the suffixes in a hashes list, then for each vertex add the edges
        prefix_hashes_list = create_prefix_hashes_lists(len(self.reads_lst[0]))
        self.num_of_vertices = len(self.reads_lst)
        for vertex in self.reads_lst:
            insert_read_prefix_hashes(vertex, prefix_hashes_list)

        for vertex in self.reads_lst:
            self.dict_graph[vertex] = find_overlap_lists(prefix_hashes_list, vertex)

    # def add_vertex(self, new_vertex):
    #     # TODO - after asking alex about optimized way to compare edges, change to that
    #     overlap_lst = []
    #     for key in self.dict_graph.keys():
    #         new_suffix_edge = get_overlap(new_vertex, key)
    #
    #         if new_suffix_edge:
    #             # new_vertex is prefix to a key
    #             overlap_lst.append(new_suffix_edge)
    #         new_prefix_edge = get_overlap(key, new_vertex)
    #
    #         if new_prefix_edge:  #
    #
    #             self.dict_graph[key].append(new_prefix_edge)
    #
    #     self.dict_graph[new_vertex] = overlap_lst
