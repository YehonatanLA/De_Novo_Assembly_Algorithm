import random
import time

# some consts
BIG_PRIME = 500000003
BASE_NUM = 4
letter_to_base_four = {'A': 0, 'C': 1, 'G': 2, 'T': 3}

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


def create_convert_list(read_size):
    convert_array = [1] * read_size
    for i in range(read_size - 2, -1, -1):
        convert_array[i] = (convert_array[i + 1] * BASE_NUM) % BIG_PRIME
    return convert_array


def get_current_time(current_time):
    print(f"time: {time.time() - current_time}")


def print_start_msg(original_str):
    print("----------------------------------------------------")
    print("De Novo Assembly Algorithm\n")
    print("Original Strand: ")
    print(original_str + "\n")
