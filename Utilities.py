import random
import time

BIG_PRIME = 500000003
letters = ['A', 'C', 'G', 'T']

def generate_string(str_len):
    return ''.join(random.choice(letters) for _ in range(str_len))


def read_random_input(original_str, str_len, window_size, num_of_reads):
    lst_of_all_reads = []
    index = 0

    while index < num_of_reads:
        start_index = random.randint(0, str_len - window_size)
        sub_strand = original_str[start_index: start_index + window_size]
        if sub_strand not in lst_of_all_reads:
            lst_of_all_reads.append(sub_strand)
            index += 1
    return lst_of_all_reads


def get_current_time(current_time):
    print(f"time: {time.time() - current_time}")


def print_start_msg(original_str):
    print("----------------------------------------------------")
    print("De Novo Assembly Algorithm\n")
    print("Original Strand: ")
    print(original_str + "\n")


def create_prefix_hashes_lists(read_size):
    prefix_hashes_list = []
    # only need to have len - 1 hash tables
    # table[i] = stores hashes from index i to end 
    for i in range(1, read_size):
        prefix_hashes_list.append({})
    return prefix_hashes_list


def insert_read_prefix_hashes(read, prefix_hashes_list):
    """
    saves in prefix_hashes_list all the different suffix hashes of the read from 1 to len(read) - 1
    :param read: the string to turn to numbers in the hash function
    :param prefix_hashes_list: a list that each index is a hash table with a number as the key and a list
           of all prefixes of different reads as the value
   return: none
    """
    hash_output = 0

    for index in range(0, len(prefix_hashes_list) - 1):
        curr_letter = read[index]
        # get hash of suffix from index to end
        hash_output = ((hash_output * 4) % BIG_PRIME + letters[curr_letter]) % BIG_PRIME
        # insert to tables
        # could be there is no items in dict with this hash output. If not, we create a new list
        prefix_index_list = []

        if hash_output in prefix_hashes_list[index - 1]:
            prefix_index_list = prefix_hashes_list[index - 1][hash_output]
        prefix_index_list.append(read)
        prefix_hashes_list[index - 1][hash_output] = prefix_index_list


def find_overlap_lists(prefix_hashes_list, vertex):
    """
    :param prefix_hashes_list: list of all hashes tables, each one of index i containing all the prefixes of length i
    of all reads
    :param vertex: the vertex that the function will check for overlap
    :return: a list of items,
    where in index i there is a list of all suffix-prefix matches of length i (the vertex is the suffix)
    """

    # [{},{}]
    overlap_lists = []
    rolling_hash_results = [1]
    hash_output = 0
    power_of_four = letters[vertex[-1]]
    vertex_len = len(vertex)

    for index in range(0, vertex_len):
        power_of_four = (power_of_four * 4) % BIG_PRIME
        rolling_hash_results.append(power_of_four)

    for index in range(1, vertex_len):
        curr_letter = vertex[vertex_len - index]
        hash_output = (hash_output + (letters[curr_letter] * rolling_hash_results[index]) % BIG_PRIME) % BIG_PRIME
        hash_output = ((hash_output * 4) % BIG_PRIME + letters[curr_letter]) % BIG_PRIME

    # for index in range(0, vertex_len):
    #     # get hash of suffix from end to index
    #     rolling_hash_results.append(hash_output)

    return overlap_lists


def is_real_overlap(suffix, prefix, overlap):
    return suffix[len(suffix) - overlap:] == prefix[0:overlap]

