import random
import time

BIG_PRIME = 500000003


def generate_string(str_len):
    letters = ['A', 'C', 'G', 'T']
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


def create_suffix_hashes_lists(reads_amount):
    suffix_hashes_list = []
    # only need to have len - 1 hash tables
    # table[i] = stores hashes from index i to end 
    for i in range(1, reads_amount):
        suffix_hashes_list.append({})
    return suffix_hashes_list


def insert_read_suffix_hashes(read, suffix_hashes_list):
    """
    saves in suffix_hashes_list all the different suffix hashes of the read from 1 to len(read) - 1
    :param read: the string to turn to numbers in the hash function
    :param suffix_hashes_list: a list that each index is a hash table with a number as the key and a list
           of all suffixes of different reads as the value
    """
    hashed_length = len(read)
    char_to_num = {'A': 0, 'C': 1, 'G': 2, 'T': 3}
    hash_output = 0

    for index in range(hashed_length - 1, 0, -1):
        curr_letter = read[index]
        # get hash of suffix from index to end
        hash_output = ((hash_output * 4) % BIG_PRIME + char_to_num[curr_letter]) % BIG_PRIME
        # insert to tables
        # could be there is no items in dict with this hash output. If not, we create a new list
        try:
            suffix_index_list = suffix_hashes_list[index - 1][hash_output]

        except KeyError:
            suffix_hashes_list[index - 1][hash_output] = []
            suffix_index_list = suffix_hashes_list[index - 1][hash_output]

        suffix_index_list.append(read[index:])
        suffix_hashes_list[index - 1][hash_output] = suffix_index_list
