
from Induced_Graph import AllOverlapGraphOptimizedByAlex
from Utilities import *
from DynamicPrograming import *

NUM_OF_TESTS = 100
NUM_OF_SUCCESSES = 0
NUM_OF_VERTICES = {}
TESTS_FAILED = []
TIME_I = 0
TIME_G = 0
TIME_DYNAMIC = 0
CURR_TEST = 0
same = 0


def final_algorithm(strand_len, read_size, real_edge_length, reads_lst, padding_positions=None):
    """

    :param strand_len:
    :param read_size:
    :param real_edge_length:
    :param reads_lst:
    :param padding_positions: padding positions is a list containing two lists:
     one is for padding reads in the start of the section,
      and the second is for padding reads at the end of the section
    :return:
    """
    global TIME_I, TIME_G, TESTS_FAILED, NUM_OF_SUCCESSES, NUM_OF_VERTICES, TIME_DYNAMIC, same
    # success = False
    # initialize data
    start_time = time.time()
    reads_lst_to_use = reads_lst

    # print_start_msg(original_strand_to_use)

    # time for initialization data
    # get_current_time(start_time)

    # build induced graph
    # TODO: I don't think we need to have two different cases for the algorithm. We're doing a new version -
    #  no need to keep the old one too
    data_for_induced_graph = AllOverlapGraphOptimizedByAlex(read_size, real_edge_length, reads_lst_to_use, padding_positions)

    induced_graph = data_for_induced_graph.build_induced_graph_from_data()
    f_i = time.time()
    finished_i = time.time() - start_time
    TIME_I += finished_i
    # induced_graph.print_graph("Induced Graph")

    # print("after induced graph:")
    # get_current_time(start_time)
    # time for building the induced graph data
    # get_current_time(start_time)

    # build final directed graph
    final_directed_graph = FinalDirectedGraph(induced_graph)
    finished_g = time.time() - f_i
    f_g = time.time()
    TIME_G += finished_g
    # print("after final directed graph:")
    # final_directed_graph.print_graph("Final Directed Graph")
    # get_current_time(start_time)
    str_list_candidate = create_guesses(final_directed_graph, strand_len)
    TIME_DYNAMIC += time.time() - f_g

    # if not string_list_candidate or original_strand not in string_list_candidate:
    #     final_directed_graph.is_success = False
    #     TESTS_FAILED.append(CURR_TEST)
    # else:
    #     final_directed_graph.is_success = True
    #     success = True
    #     NUM_OF_SUCCESSES += 1
    # print_success_or_failure(final_directed_graph.is_success)
    # get_current_time(start_time)

    # if final_directed_graph.num_of_vertices in NUM_OF_VERTICES:
    #     NUM_OF_VERTICES[int(final_directed_graph.num_of_vertices)] += 1
    # else:
    #     NUM_OF_VERTICES[int(final_directed_graph.num_of_vertices)] = 1
    # time of building the final directed_graph (should be very fast)

    # create_guesses(final_directed_graph, original_strand_to_use)
    return str_list_candidate


if __name__ == '__main__':
    time_sum = 0
    for i in range(0, NUM_OF_TESTS):
        if i % 10 == 0:
            print(f"Test Number {i}")
        CURR_TEST = i
        f = open(f"input{i}.txt", "r")
        str_len = 10000
        window_size = 50
        real_edge_len = 20
        original_str = f.readline().strip()
        reads_list = []
        for line in f:
            line = line.strip()
            reads_list.append(line)
        num_of_reads = len(reads_list)
        start_alg = time.time()
        string_list_candidate = final_algorithm(str_len, window_size, real_edge_len, reads_list)
        finish_alg = time.time()
        if not string_list_candidate or original_str not in string_list_candidate:
            TESTS_FAILED.append(CURR_TEST)
        else:
            success = True
            NUM_OF_SUCCESSES += 1

        time_sum += finish_alg - start_alg
    stats_file = open("stats2.txt", "w")
    stats_file.write("Paths num\t\t Occurences\n")
    for key, val in NUM_OF_VERTICES.items():
        stats_file.write(f"{key}\t\t\t {val}\n")

    stats_file.write("\n\n")
    stats_file.write(f"Overall success rate: \t\t\t\t {NUM_OF_SUCCESSES / (NUM_OF_SUCCESSES + len(TESTS_FAILED))}\n")
    if len(TESTS_FAILED) == 0:
        stats_file.write("No tests failed!\n")
    else:
        stats_file.write("Tests failed: \n")
        for fail in TESTS_FAILED:
            stats_file.write(f"{fail}\n")

    stats_file.write("\n\n")
    stats_file.write(f"Overall time to create graph I: {TIME_I}\n")
    stats_file.write(f"Overall time to create graph G**: {TIME_G}\n")
    stats_file.write(f"Overall time to do dynamic programming: {TIME_DYNAMIC}\n")
    stats_file.write(f"total algorithm time: {time_sum}\n")
