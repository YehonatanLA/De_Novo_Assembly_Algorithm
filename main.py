from Utilities import *
from Graph import *


def construct_I_graph(all_overlaps_graph, str_len, real_edge_len, window_size):
    """
    :param all_overlaps_graph:
    :param str_len:
    :param real_edge_len:
    :return:
    """
    # TODO
    return dict


def construct_final_directed_graph(graph_I, all_overlaps_graph, real_edge_len, window_size):
    """
    :param graph_I:
    :param all_overlaps_graph:
    :param real_edge_len:
    :return:
    """
    # TODO
    return dict


def reconstruct_string(all_overlaps_graph, str_len, real_edge_len, window_size):
    """
    first part
    :param window_size: the size of the
    :param all_overlaps_graph: the graph with all the overlaps, including possibly fakes
    :param str_len: the length of the original string
    :param real_edge_len: the length that ensures with high probability that the edge is real
    :return: the guess for the reconstructed string
    """
    # the first part - get the graph with SCC of real edges, and connect them with possibly fake edges
    induced_graph = InducedGraph(all_overlaps_graph, real_edge_len)
    print("graph I\n")
    induced_graph.print_graph()
    # graph_final_directed = construct_final_directed_graph(graph_I, all_overlaps_graph, real_edge_len, window_size)

    # part two - TODO write what happens here

    return "placeholder"


def main():
    print("starting De Novo assembly:\n")
    """
    README:
    some directions or instructions
    probably a good idea to put some of the covers and stuff in classes
    though until then they are local variables
    reads_dict - the hash table containing the different reads
    """

    """
    this part is generating the input for test  
    """
    str_len = 15
    window_size = 7
    real_edge_len = 4
    num_of_reads = 7
    original_str = generate_string(str_len)
    print(original_str + "\n")
    reads_list = read_random_input(original_str, str_len, window_size, num_of_reads)

    """
    this part is the actual algorithm  
    """
    g_star = AllOverlapsGraph(reads_list)
    print("G star:\n")
    g_star.print_graph()
    # all_overlaps_graph = all_suffix_prefix_matches(reads_list, num_of_reads) # build G*
    guess = reconstruct_string(g_star, str_len, real_edge_len, window_size)

    """
    this part is printing the results
    """

    # if guess == original_str:
    #     print("Great success!")

    # else:
    #     print("Failed to guess string")


if __name__ == '__main__':
    main()
