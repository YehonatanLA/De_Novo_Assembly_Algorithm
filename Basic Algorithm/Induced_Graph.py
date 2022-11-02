

from Utilities import *
from Graph import *


class InducedGraphAux:

    # store all the relevant data for building the induced graph
    def __init__(self, read_size, real_edge_size, reads_lst):
        self.four_inverse = find_four_inverse() # (4^(-1)) % P
        self.four_pow = create_convert_list(read_size) # [1,4,16,64,....,] each element (mod P)
        self.reads_lst = reads_lst
        self.read_size = read_size
        self.real_edge_size = real_edge_size
        self.reads_number = len(reads_lst)
        self.last_prefix_hash = [0] * self.reads_number
        self.last_suffix_hash = [0] * self.reads_number
        self.hash_of_indexes = {}
        self.threshold_value = read_size // 2

    # the function which builds the Induced graph
    def build_induced_graph_from_data(self):
        graph = Graph()
        first_step_time = time.time()
        self.insert_full_hash()
        first_step_time = time.time() - first_step_time
        print(f"first step time is {first_step_time}")
        second_step_time = time.time()
        self.second_step(graph)
        second_step_time = time.time() - second_step_time
        print(f"second step time is {second_step_time}")
        third_step_time = time.time()
        self.third_step(graph)
        third_step_time = time.time() - third_step_time
        print(f"third step time is {third_step_time}")
        sum_time = first_step_time + second_step_time + third_step_time
        print(
            f"The first part is about {first_step_time * 100 / sum_time}%\nThe second part is about"
            f" {second_step_time * 100 / sum_time}%\nThe third part is about {third_step_time * 100 / sum_time}%")
        return graph

    # first step in algorithm
    def insert_full_hash(self):
        for i in range(self.reads_number):
            hash_output = full_hash(self.reads_lst[i], 0, self.read_size - 1)
            self.last_prefix_hash[i] = hash_output

            if hash_output not in self.hash_of_indexes.keys():
                self.hash_of_indexes[hash_output] = []
            self.hash_of_indexes[hash_output].append(i)

    # second step in algorithm
    def second_step(self, graph):
        for i in range(self.reads_number):
            read = self.reads_lst[i]
            prev_hash = self.last_prefix_hash[i]
            suffix_hash = shift_right_hash(read, 1, self.read_size - 1, prev_hash, self.four_pow)
            self.last_suffix_hash[i] = suffix_hash

            if suffix_hash == NO_HASH or prev_hash == NO_HASH:
                continue

            if suffix_hash not in self.hash_of_indexes:
                self.hash_of_indexes[suffix_hash] = []

            for j in self.hash_of_indexes[suffix_hash]:

                # prefix = self.reads_lst[j][:self.read_size - 1]
                # suffix = self.reads_lst[i][1:]
                if compare_reads(self.reads_lst[j], self.reads_lst[i], 1, self.read_size - 1):
                    edge = Edge(self.read_size - 1, self.reads_lst[j])

                    graph.add_edge(self.reads_lst[i], edge)

                    prefix = self.reads_lst[j][:self.read_size - 1]
                    self.hash_of_indexes[suffix_hash].remove(j)

                    if get_length_of_longest_prefix_suffix(prefix, self.read_size - 1) >= self.threshold_value:
                        if len(graph.dict_graph[self.reads_lst[i]]) == 1:
                            del graph.dict_graph[self.reads_lst[i]]
                        else:
                            graph.dict_graph[self.reads_lst[i]].remove(edge)
                    else:
                        self.last_suffix_hash[i] = NO_HASH
                    break

    def third_step(self, graph):
        for match_len in range(self.read_size - 2, self.real_edge_size - 1, -1):
            self.hash_of_indexes = {}

            # calculate hash of prefixes
            for i in range(self.reads_number):

                if self.last_prefix_hash[i] == NO_HASH:
                    continue

                read = self.reads_lst[i]
                prev_hash = self.last_prefix_hash[i]
                hash_output = discarded_LSL_hash(read, 0, match_len, prev_hash, self.four_inverse)
                self.last_prefix_hash[i] = hash_output

                if hash_output not in self.hash_of_indexes:
                    self.hash_of_indexes[hash_output] = []

                self.hash_of_indexes[hash_output].append(i)

            for i in range(self.reads_number):
                # calculate hash of suffixes
                if self.last_suffix_hash[i] == NO_HASH:
                    continue

                read = self.reads_lst[i]
                prev_hash = self.last_suffix_hash[i]
                hash_output = discarded_MSL_hash(read, self.read_size - match_len, match_len, prev_hash, self.four_pow)
                self.last_suffix_hash[i] = hash_output

                if hash_output == NO_HASH:
                    continue

                if hash_output not in self.hash_of_indexes:
                    self.hash_of_indexes[hash_output] = []

                # check for matches
                for j in self.hash_of_indexes[hash_output]:
                    # prefix = self.reads_lst[j][:match_len]
                    # suffix = self.reads_lst[i][self.read_size - match_len:]

                    if compare_reads(self.reads_lst[j], self.reads_lst[i], self.read_size - match_len, match_len):
                        edge = Edge(match_len, self.reads_lst[j])

                        graph.add_edge(self.reads_lst[i], edge)

                        self.hash_of_indexes[hash_output].remove(j)
                        prefix = self.reads_lst[j][:match_len]

                        if get_length_of_longest_prefix_suffix(prefix, match_len) >= self.threshold_value:
                            if len(graph.dict_graph[self.reads_lst[i]]) == 1:
                                del graph.dict_graph[self.reads_lst[i]]
                            else:
                                graph.dict_graph[self.reads_lst[i]].remove(edge)
                        else:
                            self.last_prefix_hash[j] = NO_HASH
                            self.last_suffix_hash[i] = NO_HASH
                        break
        # finally, add all the remaining vertices that weren't added so far:
        for vertex in self.reads_lst:
            if vertex not in graph.dict_graph.keys():
                graph.add_vertex_with_no_edges(vertex)
