from Graph import *
from AllOverlapsGraphOptimized import *


# graph I
class InducedGraphOptimized(Graph):

    def __init__(self, pseudo_all_overlap_graph: AllOverlapGraphOptimized):
        Graph.__init__(self)
        self.convert_list = create_convert_list(pseudo_all_overlap_graph.read_size)  # need to check
        self.pseudo_all_overlap_graph = pseudo_all_overlap_graph

    def add_read_to_graph(self, read):
        hash_output = 0

        # from real edge to L-1
        for suffix_len in range(len(read) - 1, 0, -1):

            # calculate hash
            curr_number = letter_to_base_four[read[suffix_len]]
            hash_output = (hash_output + (curr_number * self.convert_list[suffix_len])) % BIG_PRIME

            # get table for len of suffix
            curr_table_index = self.pseudo_all_overlap_graph.get_table_index(suffix_len)
            curr_table = self.pseudo_all_overlap_graph.final_pseudo_graph[curr_table_index]

            # get the list from table using hash
            curr_list = curr_table[hash_output]

            # find the match
            # notice that, if list is empty nothing will happen
            # else the code will find the unique match

            number_of_matches = 0
            match = None
            for read_prefix in curr_list:
                if compare_prefix_suffix(suffix_len, read_prefix, read):
                    match = read_prefix
                    number_of_matches += 1

            if number_of_matches == 1:
                edge = Edge(suffix_len, match)
                self.dict_graph[read] = [edge]
                return

    def add_all_read_to_graph(self, reads):
        for read in reads:
            self.add_read_to_graph(read)