from FinalDirectedGraph import *
from Graph import *


def create_guess(final_directed, original_str_len):
    if final_directed.num_of_vertices == 1:
        for key in final_directed.dict_graph.keys():
            return key

    candidate_edge_sets = find_candidate_edge_sets(final_directed, original_str_len)
    return generate_possible_guesses()


def create_overlaps_mat(final_overlap_graph, num_of_vertices):
    vertices_total_len = 0

    for vertex in final_overlap_graph.dict_graph.keys():
        vertices_total_len += len(vertex)
    # overlaps_sum = W in alex's paper, and W = n - sum of len(vertex)
    overlaps_sum = vertices_total_len - original_len
    # create matrix of num_of_vertices + 1 rows and W + 1 columns
    overlaps_matrix = [[None] * (overlaps_sum + 1)] * (num_of_vertices + 1)
    overlaps_matrix[1][1] = [0]
    return overlaps_sum, overlaps_matrix


def find_candidate_edge_sets(final_overlap_graph: FinalDirectedGraph, original_len):
    """
    The function will use G** to create a guess of reconstructed string

    :param final_overlap_graph: the G** graph that the guess will be constructed from
    :return: the guess if there is one, empty string otherwise
    """

    # all_edges_list will be a list that each item of index i is a list of all edges coming out of vertex i
    num_of_vertices = final_overlap_graph.num_of_vertices
    overlaps_sum, overlaps_matrix = create_overlaps_mat(final_overlap_graph, num_of_vertices)
    vertices_list = []

    for vertex in final_overlap_graph.dict_graph.keys():
        vertices_list.append(vertex)
    # prev_weights_added will be a list of all indexes that were added above row
    prev_weights_added = {0}
    temp_added_weights = set()

    # initialize the matrix with first row of edges
    for edge in final_overlap_graph.dict_graph[vertices_list[0]]:
        edge_weight = edge.weight

        if overlaps_matrix[1][edge_weight] is None and edge_weight <= overlaps_sum:
            overlaps_matrix[1][edge_weight] = {edge_weight}
            prev_weights_added.add(edge_weight)

    # now fill up the matrix in rows two to N
    for row in range(2, num_of_vertices + 1):

        # going through all the non-empty indexes
        for not_empty_index in prev_weights_added:
            overlaps_matrix[row][not_empty_index] = {0}

            # for each index, go through all edges of vertex
            for edge in final_overlap_graph.dict_graph[vertices_list[row - 1]]:
                column_to_insert = edge.weight + not_empty_index

                if column_to_insert <= overlaps_sum:
                    if overlaps_matrix[row][column_to_insert] is None:
                        overlaps_matrix[row][not_empty_index] = {column_to_insert}
                    else:
                        overlaps_matrix[row][column_to_insert].add(column_to_insert)
                    temp_added_weights.add(column_to_insert)

        prev_weights_added.update(temp_added_weights)
        temp_added_weights = set()
