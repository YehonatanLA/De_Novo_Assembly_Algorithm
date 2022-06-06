class Edge:
    def __init__(self, weight, overlap, next_vertex):
        self.weight = weight
        self.overlap = overlap
        self.next_vertex = next_vertex

    def print_edge(self):
        print(f"next vertex: {self.next_vertex}, weight of edge: {self.weight}, overlap of edge: {self.overlap}")


class Graph:
    def __init__(self):
        self.num_of_vertices = 0
        self.dict_graph = {}

    def get_max_edge(self, vertex):
        if len(self.dict_graph[vertex]) == 0:
            return None

        max_weight = 0
        edge_to_return = self.dict_graph[vertex][0]
        for edge in self.dict_graph[vertex]:
            if max_weight < edge.weight:
                edge_to_return = edge
                max_weight = edge.weight
        return edge_to_return

    def is_unique_and_real(self, vertex, max_edge, real_read_len):
        if max_edge is None:
            return False
        for edge in self.dict_graph[vertex]:
            if edge is not max_edge and edge.next_vertex == max_edge.next_vertex:
                return False
        return max_edge.weight >= real_read_len

    def print_graph(self):
        for key, edges_lst in self.dict_graph.items():
            print(f"vertex: {key}")
            for data in edges_lst:
                data.print_edge()
            print("\n")

    def get_overlap(self, suffix_vertex, prefix_vertex):
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


# graph G star
class AllOverlapsGraph(Graph):

    def __init__(self, reads_lst):
        Graph.__init__(self)
        self.reads_lst = reads_lst
        self.add_vertices()

    def add_vertex(self, new_vertex):
        """
        :param new_vertex: the vertex to add to graph
        :return: void
        TODO - after asking alex about optimized way to compare edges, change to that
        """
        overlap_lst = []
        for key in self.dict_graph.keys():
            new_suffix_edge = self.get_overlap(new_vertex, key)

            if new_suffix_edge:
                # new_vertex is prefix to a key
                overlap_lst.append(new_suffix_edge)
            new_prefix_edge = self.get_overlap(key, new_vertex)

            if new_prefix_edge:  #

                self.dict_graph[key].append(new_prefix_edge)

        self.dict_graph[new_vertex] = overlap_lst

    def add_vertices(self):
        for vertex in self.reads_lst:
            self.add_vertex(vertex)


# graph I
class InducedGraph(Graph):
    def __init__(self, all_overlap_graph, real_read_len):
        Graph.__init__(self)

        # TODO: write the algorithm with linear complexity, based on the way to build AllOverlapsGraph

        for vertex, list_of_edges in all_overlap_graph.dict_graph.items():
            max_edge = all_overlap_graph.get_max_edge(vertex)

            if all_overlap_graph.is_unique_and_real(vertex, max_edge, real_read_len):
                self.dict_graph[vertex] = [max_edge]



# G star star
class FinalDirectedGraph(Graph):
    def __init__(self, induced_graph):
        Graph.__init__(self)
        self.roots = {}

        for vertex in induced_graph.dict_graph.keys():
            self.roots[vertex] = True

        for vertex, list_of_edges in induced_graph.dict_graph.items():
            for edge in list_of_edges:
                self.roots[edge.next_vertex] = False

        # check it later
        roots = {vertex: status for vertex, status in self.roots.items() if status}

        for root in roots:
            new_vertex = root
            # TODO: finish

