import time

from Induced_Graph import AllOverlapGraphOptimizedBYAlex
from Utilities import *
from FinalDirectedGraph import *
from DynamicPrograming import *

NUM_OF_TESTS = 300


def final_algorithm(strand_len, read_size, real_edge_length, number_of_reads, original_strand="", reads_lst=None):
    # initialize data
    start_time = time.time()

    original_strand_to_use = original_strand
    reads_lst_to_use = reads_lst

    if original_strand == "":
        original_strand_to_use = generate_string(strand_len)

    if reads_lst is None:
        reads_lst_to_use = read_random_input_improve2(original_strand_to_use, strand_len, read_size, number_of_reads)

    print_start_msg(original_strand_to_use)

    # time for initialization data
    # get_current_time(start_time)

    # build induced graph
    data_for_induced_graph = AllOverlapGraphOptimizedBYAlex(read_size, real_edge_length, reads_lst_to_use)
    induced_graph = data_for_induced_graph.build_induced_graph_from_data()
    # induced_graph.print_graph("Induced Graph")

    # print("after induced graph:")
    # get_current_time(start_time)
    # time for building the induced graph data
    # get_current_time(start_time)

    # build final directed graph
    final_directed_graph = FinalDirectedGraph(induced_graph, original_strand_to_use)
    # print("after final directed graph:")
    final_directed_graph.print_graph("Final Directed Graph")
    get_current_time(start_time)
    string_list_candidate = create_guesses(final_directed_graph, strand_len)

    if not string_list_candidate or original_strand not in string_list_candidate:
        final_directed_graph.is_success = False
    else:
        final_directed_graph.is_success = True
    print_success_or_failure(final_directed_graph.is_success)
    get_current_time(start_time)

    # time of building the final directed_graph (should be very fast)

    # create_guesses(final_directed_graph, original_strand_to_use)


if __name__ == '__main__':
    time_sum = 0
    for i in range(0, 300):
        f = open(f"input{i}.txt", "r")
        str_len = 10000
        window_size = 100
        real_edge_len = 20
        original_str = f.readline().strip()
        reads_list = []
        for line in f:
            line = line.strip()
            reads_list.append(line)
        num_of_reads = len(reads_list)
        start_alg = time.time()
        final_algorithm(str_len, window_size, real_edge_len, num_of_reads, original_str, reads_list)
        finish_alg = time.time()
        time_sum += finish_alg - start_alg
    print(f"total algorithm time: {time_sum}")
