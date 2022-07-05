from Graph import Graph
from Utilities import create_convert_list
from AllOverlapsGraphOptimized import *

# graph I
class InducedGraphOptimized(Graph):

    def __init__(self, pseudo_all_overlap_graph):
        Graph.__init__(self)
        self.convert_list = create_convert_list(pseudo_all_overlap_graph.read_size)  # need to check
        self.pseudo_all_overlap_graph = pseudo_all_overlap_graph

    # def add_read_to_graph(self,read):
    #    for i in range(self.pseudo_all_overlap_graph.)

