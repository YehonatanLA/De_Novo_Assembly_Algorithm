from Graph import Graph


# graph I
class InducedGraph(Graph):

    def __init__(self, all_overlap_graph, real_read_len):
        Graph.__init__(self)
        self.all_overlap_graph = all_overlap_graph
        # TODO: write the algorithm with linear complexity, based on the way to build AllOverlapsGraph

        for vertex, list_of_edges in self.all_overlap_graph.dict_graph.items():
            max_edge = self.get_max_edge(vertex)

            if self.is_unique_and_real(vertex, max_edge, real_read_len):
                self.dict_graph[vertex] = [max_edge]

    def get_max_edge(self, vertex):

        if not self.all_overlap_graph.dict_graph[vertex]:
            return None

        max_weight = 0
        edge_to_return = self.all_overlap_graph.dict_graph[vertex][0]
        for edge in self.all_overlap_graph.dict_graph[vertex]:
            if max_weight < edge.weight:
                edge_to_return = edge
                max_weight = edge.weight
        return edge_to_return

    def is_unique_and_real(self, vertex, max_edge, real_read_len):
        if max_edge is None:
            return False
        for edge in self.all_overlap_graph.dict_graph[vertex]:
            if edge is not max_edge and edge.next_vertex == max_edge.next_vertex:
                return False
        return max_edge.weight >= real_read_len
string = "aaabc"
