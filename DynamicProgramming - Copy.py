from FinalDirectedGraph import *
from Graph import *


def create_guess(final_overlap_graph, original_len):
    """
    The function will use G** to create a guess of reconstructed string

    :param final_overlap_graph: the G** graph that the guess will be constructed from
    :return: the guess if there is one, empty string otherwise
    """

    if final_overlap_graph.number_of_vertices == 1:
        """ is there a better than this to return the only key?"""
        for key in final_overlap_graph.dict_graph.keys():
            return key

    # all_edges_list will be a list that each item of index i is a list of all edges coming out of vertex i
    all_edges_list = [final_overlap_graph.dict_graph[vertex] for vertex in final_overlap_graph.dict_graph.keys()]
    guess = ""
    vertices_total_len = 0

    for vertex in final_overlap_graph.dict_graph.keys():
        vertices_total_len += len(vertex)
    num_of_vertices = final_overlap_graph.number_of_vertices
    # overlaps_sum = W in alex's paper, and W = n - sum of len(vertex)
    overlaps_sum = original_len - vertices_total_len
    overlaps_matrix = [[] * (num_of_vertices + 1) for _ in range(overlaps_sum)]

    overlaps_matrix[1][0] = 0
    for edge in all_edges_list[0]:




    # A Dynamic Programming solution for subset
    # sum problem Returns true if there is a subset of
    # set[] with sun equal to given sum

    # Returns true if there is a subset of set[]
    # with sum equal to given sum
