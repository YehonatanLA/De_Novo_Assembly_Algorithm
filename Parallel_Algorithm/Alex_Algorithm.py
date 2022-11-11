from Parallel_Algorithm.Induced_Graph import Induced_Graph_Aux
from Parallel_Algorithm.DynamicPrograming import *


def alex_algorithm(strand_len, read_size, real_edge_length, reads_lst, padding_positions):
    """
    :param strand_len: length of the original strand
    :param read_size: length of a read
    :param real_edge_length: the value T which is explained in the article
    :param reads_lst: the list of all reads
    :param padding_positions: padding positions is a list containing two lists:
     one is for padding reads in the start of the section,
     and the second is for padding reads at the end of the section
    :return: a list of possible solutions
    """

    # build induced graph
    data_for_induced_graph = Induced_Graph_Aux(read_size, real_edge_length, reads_lst, padding_positions)
    induced_graph = data_for_induced_graph.build_induced_graph_from_data()


    # build final directed graph
    final_directed_graph = FinalDirectedGraph(induced_graph)

    # dynamic programming algorithm in order to find possible solutions
    str_list_candidate = create_guesses(final_directed_graph, strand_len)

    return str_list_candidate
