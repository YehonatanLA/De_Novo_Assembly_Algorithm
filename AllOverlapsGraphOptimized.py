from Utilities import *

class AllOverlapGraphOptimized:

    def __init__(self, reads, real_edge_len, read_size):
        self.reads = reads
        self.real_edge_len = real_edge_len
        self.read_size = read_size
        self.final_pseudo_graph = self.get_pseudo_graph()

    def initialized_prefix_hashes_lists(self):
        number_of_tables = self.read_size - self.real_edge_len
        return [{} for _ in range(0, number_of_tables)]

    def get_table_index(self, index):
        return index - self.real_edge_len

    def insert_read_to_table(self, prefix_hashes_list, read):
        hash_output = 0
        for prefix_len in range(0, self.read_size):

            # calculate hash
            curr_number = letter_to_base_four[read[prefix_len]]
            hash_output = ((hash_output * BASE_NUM) % BIG_PRIME + curr_number) % BIG_PRIME

            if prefix_len >= self.real_edge_len - 1:

                # get the specific hash table
                index_of_prefix_table = self.get_table_index(prefix_len)
                curr_prefix_table = prefix_hashes_list[index_of_prefix_table]

                # put the read inside the hash
                if hash_output not in curr_prefix_table:
                    curr_prefix_table[hash_output] = []
                curr_prefix_table[hash_output].append(read)

    # it is a pseudo graph
    # in this function we insert all the reads to prefix hashes list
    def get_pseudo_graph(self):
        prefix_hashes_list = self.initialized_prefix_hashes_lists()
        for read in self.reads:
            self.insert_read_to_table(read, prefix_hashes_list)
        return prefix_hashes_list
