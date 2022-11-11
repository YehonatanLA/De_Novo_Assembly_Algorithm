import typing
from Parallel_Algorithm.FinalDirectedGraph import *

list_of_candidates = []


def create_guesses(final_directed: FinalDirectedGraph, original_str_len):
    global list_of_candidates
    """The function finds the candidate edge sets that have n-1 edges and at most one edge from each vertex, 
    and filters out any set that isn't a path between the vertices in final_directed graph :param final_directed: A 
    graph holding in the vertices parts of reconstructed string, and for edges holds the overlaps between two 
    vertices
    :param original_str_len: The length of the original string 
    :return: A list of the strings that the filtered edge sets represent, potentially the original string, 
    or None if there are no potential string candidates """
    if final_directed.get_number_of_vertices() == 0:
        return None

    if final_directed.get_number_of_vertices() == 1:
        for key in final_directed.dict_graph.keys():
            return [key]
    vertices_list = []
    vertex_to_index = {}
    i = 0

    for vertex in final_directed.dict_graph.keys():
        vertices_list.append(vertex)
        vertex_to_index[vertex] = i
        i += 1

    candidate_edge_sets = find_candidate_edge_sets(final_directed, original_str_len, vertices_list, vertex_to_index)
    if candidate_edge_sets is None:
        return None
    filtered_edge_sets = filter_edge_candidate_sets(candidate_edge_sets, vertex_to_index)
    list_of_candidates = []
    if len(filtered_edge_sets) == 0:
        return None
    return edge_sets_to_string_list(filtered_edge_sets, vertex_to_index)


# First part of sub-functions, finding the candidate edge sets
# STARTS HERE


def find_candidate_edge_sets(final_overlap_graph: FinalDirectedGraph, original_len, vertices_list, vertex_to_index):
    """
    :param vertex_to_index: A hash, for a given vertex find the index of it in the vertices list
    :param vertices_list: A list of vertices indexed.
    :param final_overlap_graph: A graph holding in the vertices parts of reconstructed string,
           and for edges holds the overlaps between two vertices
    :param original_len: The length of the string that needs to be reconstructed.
    :return: A list of candidate edge sets that are of length n-1 and guaranties that each vertex has at most one edge
             coming out of it (from the candidate set). Each edge set will be a list of weights, where a weight in index
             i will represent an edge of same weight out of vertex i. Or None if no candidate subset was found.
    """

    # all_edges_list will be a list that each item of index i is a list of all edges coming out of vertex i
    num_of_vertices = final_overlap_graph.get_number_of_vertices()
    overlaps_sum, overlaps_matrix = create_overlaps_mat(final_overlap_graph, num_of_vertices, original_len)

    # if overlap_sum is smaller than the length of the original strand, then the reads didn't cover the entire strand
    if overlaps_sum <= 0:
        return None

    overlaps_matrix = fill_overlap_matrix(final_overlap_graph, overlaps_matrix, vertices_list, overlaps_sum,
                                          num_of_vertices)
    if overlaps_matrix[num_of_vertices][overlaps_sum] is None:
        return None
    backtrack_all_candidate_edge_sets(overlaps_matrix, final_overlap_graph, num_of_vertices,
                                      [None for _ in range(num_of_vertices)], False, num_of_vertices, overlaps_sum,
                                      vertices_list, vertex_to_index, 0)
    return list_of_candidates


def create_overlaps_mat(final_overlap_graph: FinalDirectedGraph, num_of_vertices, original_len):
    """
    :
    :param final_overlap_graph: A graph holding in the vertices parts of reconstructed string,
           and for edges holds the overlaps between two vertices
    :param num_of_vertices: The number of vertices that final_overlap_graph has.
    :param original_len: The length of the string that needs to be reconstructed.
    :return: The sum of all overlap weights needed,
             and a matrix of size (rows: num_of_vertices + 1, columns: overlaps_sum + 1)
    """
    vertices_total_len = 0

    for vertex in final_overlap_graph.dict_graph.keys():
        vertices_total_len += len(vertex)
    # overlaps_sum = W in alex's paper,
    # and the equation [W = sum of vertices - n] will be if reads covered all of strand
    overlaps_sum = vertices_total_len - original_len
    # create matrix of num_of_vertices + 1 rows and W + 1 columns
    overlaps_matrix = [[None for _ in range(overlaps_sum + 1)] for _ in range(num_of_vertices + 1)]
    return overlaps_sum, overlaps_matrix


def fill_overlap_matrix(final_overlap_graph: FinalDirectedGraph, overlaps_matrix, vertices_list, overlaps_sum,
                        num_of_vertices):
    """
    The function fills up the matrix in the next order:
        1. For the first vertex in the vertices_list, for each edge out of it update matrix to matrix[1][edge.weight]
        2. For all other vertices in order, find every index from previous row that is not empty and put 0 in column of
           index for current row (matrix[previous_row][not empty index] = 0).
        3. For each edge out of vertex, add (edge.weight) to set of weights
           in cell matrix[vertex_num][edge.weight + non-empty index].

    :param final_overlap_graph: The graph holding in the vertices parts of reconstructed string,
           and for edges holds the overlaps between two vertices
    :param overlaps_matrix: The matrix that will store edge weights, starts filling weights from row 1 until last row
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
    # now fill up the matrix in rows 2 to N
    for row in range(2, num_of_vertices + 1):

        # going through all the non-empty indexes
        for not_empty_index in prev_weights_added:

            if overlaps_matrix[row][not_empty_index] is not None:
                overlaps_matrix[row][not_empty_index].add(0)
            else:
                overlaps_matrix[row][not_empty_index] = {0}

            # for each index, go through all edges of vertex
            for edge in final_overlap_graph.dict_graph[vertices_list[row - 1]]:
                column_to_insert = edge.weight + not_empty_index

                if column_to_insert <= overlaps_sum:
                    if overlaps_matrix[row][column_to_insert] is None:
                        overlaps_matrix[row][column_to_insert] = {edge.weight}
                    else:
                        overlaps_matrix[row][column_to_insert].add(edge.weight)
                    temp_added_weights.add(column_to_insert)

        prev_weights_added.update(temp_added_weights)
        temp_added_weights = set()
    return overlaps_matrix


def backtrack_all_candidate_edge_sets(overlaps_matrix, final_overlap_graph: FinalDirectedGraph, num_of_vertices,
                                      curr_edges_list, passed_zero, curr_row, curr_column, vertices_list,
                                      vertex_to_index, lst_edges_count):
    """
    The function backtracks the matrix in search for candidate edge sets in the following order:
    1. If the function reached row 0 of the matrix, if curr_edges_list has num_of_vertices - 1 edges in list,
       in which case the edge set will be permanently stored, otherwise it is unsuccessful and the function returns
    2. Otherwise, row >= 0 and  the function checks if the weights in overlaps_matrix[curr_row][curr_column] have edges
       of same weight from the current vertex. If so, try to add them to the list and go into recursion, otherwise try
       recursion with 0 (up to one 0 per list)

    :param overlaps_matrix:
           The matrix holding all the weights of edges out of vertices the backtracking function will go through
           holding in each a set of weights that got to this cell
    :param final_overlap_graph: A graph holding in the vertices parts of reconstructed string,
           and for edges holds the overlaps between two vertices
    :param num_of_vertices: The number of vertices
    :param curr_edges_list: In the current iteration of the backtracking,
           hold a list that has the current candidate edges
    :param passed_zero: Boolean that represents if not taken an edge from vertex in one of previous rows
    :param curr_row: The current row of the backtracking
    :param curr_column: The current column of the backtracking
    :param vertices_list: A order of the vertices in a list
    :param lst_edges_count: counts how many edges were added to curr_edges_list
    :param vertex_to_index: A mapping of vertices to indexes based on the vertices_list
    :returns this doesn't return but rather store arrays of length of vertices amount the possible edge lists
    """

    if lst_edges_count == num_of_vertices - 1 and curr_column == 0:
        # successful edge set
        list_of_candidates.append(list(curr_edges_list))
        return

    if curr_row == 0:
        # unsuccessful and made it to row 0, passing all possible rows
        return

    curr_vertex = vertices_list[curr_row - 1]

    for weight in overlaps_matrix[curr_row][curr_column]:
        # try with edge from vertex
        if weight > 0:

            for edge in final_overlap_graph.dict_graph[curr_vertex]:
                if edge.weight == weight:
                    index_to_insert = vertex_to_index[curr_vertex]
                    curr_edges_list[index_to_insert] = edge
                    backtrack_all_candidate_edge_sets(overlaps_matrix, final_overlap_graph, num_of_vertices,
                                                      curr_edges_list, passed_zero, curr_row - 1,
                                                      curr_column - weight, vertices_list, vertex_to_index,
                                                      lst_edges_count + 1)

                    curr_edges_list[index_to_insert] = None

    if not passed_zero and 0 in overlaps_matrix[curr_row][curr_column]:
        # try without edge from vertex
        backtrack_all_candidate_edge_sets(overlaps_matrix, final_overlap_graph, num_of_vertices, curr_edges_list, True,
                                          curr_row - 1, curr_column, vertices_list, vertex_to_index, lst_edges_count)


# ENDS HERE

# Second part, filtering out the candidates and turning the vertices lists into strings
# STARTS HERE


def filter_edge_candidate_sets(candidate_edge_sets: typing.List[typing.List[Edge]], vertex_to_index):
    """
    :
    :param candidate_edge_sets: A list of candidate edges, representing the possible path of vertices
    :param vertex_to_index: A mapping of vertices to indexes based on their position in vertices_list
    :return: All edge sets that have a root, for all vertices in_degree(vertex) <= 1, and no cycles in path
    """
    filtered_edge_sets = list()
    for edge_list in candidate_edge_sets:
        root = find_filtered_root(vertex_to_index, edge_list)
        if root is None:
            continue

        curr_vertex = root
        been_to_node_arr = [False for _ in range(len(vertex_to_index))]
        valid_set = True

        for i in range(0, len(vertex_to_index) - 1):
            # this checks if it's the last vertex and there haven't been len(vertices_amount) - 1 iterations,
            # meaning there is no one connected component
            if edge_list[vertex_to_index[curr_vertex]] is None:
                valid_set = False
                break

            next_vertex = edge_list[vertex_to_index[curr_vertex]].next_vertex
            # checks if the next node has been visited before, meaning the set is cyclic
            if been_to_node_arr[vertex_to_index[next_vertex]]:
                valid_set = False
                break

            been_to_node_arr[vertex_to_index[next_vertex]] = True
            curr_vertex = next_vertex

        if valid_set:
            # adding root to first item, so it will be easier finding the path later
            edge_list.insert(-1, Edge(0, root))
            filtered_edge_sets.append(edge_list)

    return filtered_edge_sets


def find_filtered_root(vertex_to_index, edge_list):
    """
    :param vertex_to_index: A mapping of vertices to indexes based on their position in vertices_list
    :param edge_list: A list of edges, where an edge in edge_list[i] means that the edge is from vertex in index i in
    vertices_list
    :return: The root of candidate path if one exists, otherwise None
    """
    root = None
    has_in_degree_arr = [False for _ in range(len(vertex_to_index))]

    # filling in degree of vertices
    for i in range(0, len(vertex_to_index)):
        if edge_list[i] is None:
            continue
        next_vertex = edge_list[i].next_vertex

        if has_in_degree_arr[vertex_to_index[next_vertex]]:
            # found a vertex with in degree greater than 1, no possible string can be reconstructed
            return None
        has_in_degree_arr[vertex_to_index[next_vertex]] = True

    for vertex, index in vertex_to_index.items():
        if not has_in_degree_arr[index]:
            if root is not None:
                # found at least two vertices with in degree 0, no possible string can be reconstructed
                return None
            else:
                root = vertex
    return root


def edge_sets_to_string_list(filtered_edge_sets, vertex_to_index):
    """
    :param filtered_edge_sets: A list of edges
    :param vertex_to_index: A list of edges, where an edge in edge_list[i] means that the edge is from vertex in index i in
    vertices_list
    :return: A set of potential strings that are equal to the original string
    """
    strings = set()

    for edge_list in filtered_edge_sets:
        # has to be a root since there is at least two vertices, the root is stored as last edge
        # However, since list() c'tor creates a None object as last object of list, index -2 is the last edge added
        node = edge_list[-2].next_vertex
        del edge_list[-2]
        curr_edge = edge_list[vertex_to_index[node]]
        candidate_str = node
        while curr_edge is not None:
            node = curr_edge.next_vertex
            candidate_str = "".join((candidate_str, node[curr_edge.weight:]))
            curr_edge = edge_list[vertex_to_index[node]]

        strings.add(candidate_str)
    if len(strings) == 0:
        return None
    return strings

# ENDS HERE
