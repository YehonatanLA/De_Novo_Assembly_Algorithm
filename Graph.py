import difflib


@staticmethod
def get_overlap(suffix_vertex, prefix_vertex):
    """
    :param suffix_vertex:
    :param prefix_vertex:
    :return: new edge base on the overlap of 2 vertices(2 strings)
    """
    s = difflib.SequenceMatcher(None, suffix_vertex, prefix_vertex)
    pos_a, pos_b, size = s.find_longest_match(0, len(suffix_vertex), 0, len(prefix_vertex))
    return Edge(size, suffix_vertex[pos_a:pos_a + size], prefix_vertex)


class Edge:
    def __init__(self, weight, overlap, next_vertex):
        self.weight = weight
        self.overlap = overlap
        self.vertex = next_vertex


class Graph:
    def __init__(self):
        self.num_of_vertices = 0
        self.dict_graph = {}


class All_Overlaps_Graph(Graph):

    def __init__(self, reads_lst):
        self.reads_lst = reads_lst

    def add_vertex(self, new_vertex):
        """
        :param new_vertex: the vertex to add to graph
        :return: void
        TODO - after asking alex about optimized way to compare edges, change to that
        """
        overlap_lst = []
        for key in self.dict_graph.keys():
            new_suffix_edge = get_overlap(new_vertex, key)

            if new_suffix_edge:
                # new_vertex is prefix to a key
                overlap_lst.append(new_suffix_edge)
            new_prefix_edge = self.get_overlap(key, new_vertex)

            if new_prefix_edge:
                self.dict_graph[key].append(new_prefix_edge)

        self.dict_graph[new_vertex] = overlap_lst

    def add_vertices(self):
        for vertex in self.reads_lst:
            self.add_vertex(vertex)
