from FinalDirectedGraph import *

list_of_candidates = []


def create_guess(final_directed: FinalDirectedGraph, original_str_len):
    """
    The function finds the candidate edge sets that have n-1 edges and at most one edge from each vertex,
    and filters out any set that isn't a path between the vertices in final_directed graph
    :param final_directed: The graph holding in the vertices parts of reconstructed string,
           and for edges holds the overlaps between two vertices (up to a certain length)
    :param original_str_len: The length of the reconstructed string
    :return: A list of the strings that the filtered edge sets represent
    """
    if final_directed.num_of_vertices == 1:
        for key in final_directed.dict_graph.keys():
            return key
    vertices_list = []

    for vertex in final_directed.dict_graph.keys():
        vertices_list.append(vertex)

    candidate_edge_sets = find_candidate_edge_sets(final_directed, original_str_len, vertices_list)
    if candidate_edge_sets is None:
        return None
    filtered_edge_sets = filter_edge_candidate_sets()
    return edge_sets_to_string_list(filtered_edge_sets)


def create_overlaps_mat(final_overlap_graph: FinalDirectedGraph, num_of_vertices, original_len):
    """
    :param final_overlap_graph: The graph holding in the vertices parts of reconstructed string,
           and for edges holds the overlaps between two vertices (up to a certain length)
    :param num_of_vertices: The number of vertices that final_overlap_graph has.
    :param original_len: The length of the string that needs to be reconstructed.
    :return: The sum of all overlap weights needed, and a matrix of size (num_of_vertices + 1, overlaps_sum + 1)

    """
    vertices_total_len = 0

    for vertex in final_overlap_graph.dict_graph.keys():
        vertices_total_len += len(vertex)
    # overlaps_sum = W in alex's paper, and W = n - sum of len(vertex)
    overlaps_sum = vertices_total_len - original_len
    # create matrix of num_of_vertices + 1 rows and W + 1 columns
    overlaps_matrix = [[None] * (overlaps_sum + 1)] * (num_of_vertices + 1)
    return overlaps_sum, overlaps_matrix


def fill_overlap_matrix(final_overlap_graph: FinalDirectedGraph, overlaps_matrix, vertices_list, overlaps_sum,
                        num_of_vertices):
    """
    The function fills up the matrix in the next order:
        1. Set an order to the vertices
        2. For the first vertex in the order, for each edge out of it update matrix to matrix[1][edge.weight]
        3. For all other vertices in order, find every index from previous row that is not empty and put 0 in column of
           index for current row. for each edge out of vertex, add (edge.weight) to set of weights
           in cell matrix[vertex_num][edge.weight + non-empty index].
    :param final_overlap_graph: The graph holding in the vertices parts of reconstructed string,
           and for edges holds the overlaps between two vertices (up to a certain length)
    :param overlaps_matrix: The matrix that will store edge weights
    :param vertices_list: A list of vertices that are in final_overlap_graph
    :param overlaps_sum: The sum of overlaps needed to properly construct the string.
    :param num_of_vertices: number of vertices in final_overlap_graph
    :return: The newly filled matrix
    """
    # prev_weights_added will be a list of all indexes that were added above row
    prev_weights_added = {0}
    overlaps_matrix[1][0] = {0}

    # initialize the matrix with first row of edges
    for edge in final_overlap_graph.dict_graph[vertices_list[0]]:
        edge_weight = edge.weight

        if overlaps_matrix[1][edge_weight] is None and edge_weight <= overlaps_sum:
            overlaps_matrix[1][edge_weight] = {edge_weight}
            prev_weights_added.add(edge_weight)

    temp_added_weights = set()
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
    return overlaps_matrix


def backtrack_all_candidate_edge_sets(overlaps_matrix, final_overlap_graph: FinalDirectedGraph, num_of_vertices,
                                      curr_edges_list, passed_zero, curr_row, curr_column, vertices_list):
    """
    :param vertices_list: a listing of the vertices which the edges will be based on
           (vertex in index i will be represented by edge in index i in curr_edges_list)
    :param final_overlap_graph: The graph holding in the vertices parts of reconstructed string,
           and for edges holds the overlaps between two vertices (up to a certain length)
    :param overlaps_matrix: The matrix holding all the weights the backtracking function will go through
    :param num_of_vertices: The number of vertices
    :param curr_edges_list: In the current iteration of the backtracking, hold a list that has the current edges
           in candidate solution
    :param passed_zero: Boolean that represents if not taken an edge from vertex in one of previous rows
    :param curr_row: The current row of the backtracking
    :param curr_column: The current column of the backtracking
    """
    # TODO: currently, list_of_candidates is a global variable and this will ensure that adding a new set
    #  to the list will work in backtracking. However, I suspect that putting it as a local variable might also work
    #  since it is a pointer at the end of the day. So if you find that it will work with local,
    #  I suggest you change it.

    if len(curr_edges_list) == num_of_vertices - 1 and curr_column == 0:
        # successful edge set
        list_of_candidates.append(list(curr_edges_list))
        return

    if curr_row == 0:
        # unsuccessful and made it to row 1
        return

    curr_vertex = vertices_list[curr_row]

    for weight in overlaps_matrix[curr_row][curr_column]:
        # try with edge from vertex
        if weight > 0:
            
            for edge in final_overlap_graph.dict_graph[curr_vertex]:
                if edge.weight == weight:
                    backtrack_all_candidate_edge_sets(overlaps_matrix, final_overlap_graph, num_of_vertices,
                                                      curr_edges_list.insert(0, edge), passed_zero, curr_row - 1,
                                                      curr_column - weight, vertices_list)
                    del curr_edges_list[0]

    if not passed_zero:
        # try without edge from vertex
        backtrack_all_candidate_edge_sets(overlaps_matrix, final_overlap_graph, num_of_vertices, curr_edges_list, True,
                                          curr_row - 1, curr_column, vertices_list)


def find_candidate_edge_sets(final_overlap_graph: FinalDirectedGraph, original_len, vertices_list):
    """
    :param vertices_list: The list of vertices indexed.
    :param final_overlap_graph: The graph holding in the vertices parts of reconstructed string,
           and for edges holds the overlaps between two vertices (up to a certain length).
    :param original_len: The length of the string that needs to be reconstructed.
    :return: A list of candidate edge sets that are of length n-1 and guaranties that each vertex has at most one edge
             coming out of it (from the candidate set). Each edge set will be a list of weights, where weight in index
             i will represent the out edge of same weight of vertex i. Or None if no candidate subset was found.
    """

    # all_edges_list will be a list that each item of index i is a list of all edges coming out of vertex i
    num_of_vertices = final_overlap_graph.num_of_vertices
    overlaps_sum, overlaps_matrix = create_overlaps_mat(final_overlap_graph, num_of_vertices, original_len)

    # TODO: will the overlap matrix be filled outside the function or do we need to assign the matrix again?
    overlaps_matrix = fill_overlap_matrix(final_overlap_graph, overlaps_matrix, vertices_list, overlaps_sum,
                                          num_of_vertices)
    if overlaps_matrix[num_of_vertices][overlaps_sum] is None:
        return None
    backtrack_all_candidate_edge_sets(overlaps_matrix, final_overlap_graph, num_of_vertices, [], False, num_of_vertices,
                                      overlaps_sum, vertices_list)
    return list_of_candidates
