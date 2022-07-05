from DynamicProgramming import *
# from AllOverlapsGraph import *
from InducedGraph import *
from FinalDirectedGraph import *
from Utilities import *


def final_algorithm():
    # initialize parameters
    str_len = 50
    window_size = 8
    real_edge_len = 4
    num_of_reads = 30
    current_time = time.time()

    # generate reads ,original string
    original_str = generate_string(str_len)
    reads_list = read_random_input(original_str, str_len, window_size, num_of_reads)

    # this part is the actual algorithm
    print_start_msg(original_str)

    g_star = AllOverlapsGraph(reads_list)
    g_star.print_graph(title="Graph G*")
    get_current_time(current_time)

    induced_graph = InducedGraph(g_star, real_edge_len)
    induced_graph.print_graph(title="Graph I")
    get_current_time(current_time)

    final_directed = FinalDirectedGraph(induced_graph)
    final_directed.print_graph(title="Graph G**")
    get_current_time(current_time)

    # TODO:
    #       1. compare reads using hash
    #       2. the horrible last part

    print(original_str)

    # -----------------------------------------------------------------------
    possible_guesses = create_guess(final_directed, len(original_str))
    if original_str in possible_guesses:
        print("SUCCESS")
    else:
        print("MAYBE ANOTHER TIME")
    # -----------------------------------------------------------------------


if __name__ == '__main__':
    final_algorithm()
