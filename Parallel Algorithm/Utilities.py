import random
import time
from enum import Enum

# some consts
BIG_PRIME = 500000003
BASE_NUM = 4
letter_to_base_four = {'A': 0, 'C': 1, 'G': 2, 'T': 3}
NO_HASH = -1


class Position(Enum):
    START = 0
    END = 1
    NONE = 2


def generate_string(str_len):
    letters = [key for key in letter_to_base_four.keys()]
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


def read_random_input_improve(original_str, str_len, window_size, num_of_reads):
    reads_left = [i for i in range(0, str_len - window_size + 1)]
    lst_of_all_reads = []
    index = 0
    while index < num_of_reads:
        print(index)
        pseudo_start_index = random.randint(0, len(reads_left) - 1)
        start_index = reads_left[pseudo_start_index]
        sub_strand = original_str[start_index: start_index + window_size]
        lst_of_all_reads.append(sub_strand)
        reads_left.remove(start_index)
        index += 1
    return lst_of_all_reads


def read_random_input_improve2(original_str, str_len, window_size, num_of_reads):
    reads_left = [i for i in range(0, str_len - window_size + 1)]
    lst_of_all_reads = []
    index = 0
    while index < num_of_reads:
        start_index = random.choice(reads_left)
        sub_strand = original_str[start_index: start_index + window_size]
        lst_of_all_reads.append(sub_strand)
        reads_left.remove(start_index)
        index += 1
        if index % 10000 == 0:
            print(index)
    return lst_of_all_reads


def create_convert_list(read_size):
    convert_array = [1] * read_size
    for i in range(1, read_size):
        convert_array[i] = (convert_array[i - 1] * BASE_NUM) % BIG_PRIME
    return convert_array


def compare_prefix_suffix(prefix_suffix_len, read_prefix, read_suffix):
    for i in range(prefix_suffix_len):
        if read_prefix[i] != read_suffix[len(read_suffix) + i - prefix_suffix_len]:
            return False
    return True


def find_four_inverse():
    return pow(BASE_NUM, -1, BIG_PRIME)


def get_current_time(current_time):
    print(f"time: {time.time() - current_time}\n")


def print_start_msg(original_str):
    print("----------------------------------------------------")
    print("De Novo Assembly Algorithm\n")
    print("Original Strand: ")
    print(original_str + "\n")
    print("----------------------------------------------------")


def print_success_or_failure(is_success):
    if is_success:
        print("SUCCESS")
    else:
        print("FAILURE")


def full_hash(read, pos, length):
    hash_output = 0
    for i in range(length):
        curr_number = letter_to_base_four[read[i + pos]]
        hash_output = (((hash_output * BASE_NUM) % BIG_PRIME) + curr_number) % BIG_PRIME
    return hash_output


def shift_right_hash(read, pos, length, prev_hash, four_pow):
    curr_number_to_add = letter_to_base_four[read[pos + length - 1]]
    curr_number_to_sub = (letter_to_base_four[read[pos - 1]] * four_pow[length - 1]) % BIG_PRIME
    hash_output = ((prev_hash - curr_number_to_sub) * BASE_NUM) % BIG_PRIME
    return (hash_output + curr_number_to_add) % BIG_PRIME


def discarded_MSL_hash(read, pos, length, prev_hash, four_pow):
    curr_number_to_sub = (letter_to_base_four[read[pos - 1]] * four_pow[length]) % BIG_PRIME
    return (prev_hash - curr_number_to_sub) % BIG_PRIME


def discarded_LSL_hash(read, pos, length, prev_hash, four_inv):
    curr = (prev_hash - letter_to_base_four[read[pos + length]]) % BIG_PRIME
    return (curr * four_inv) % BIG_PRIME


def get_length_of_longest_prefix_suffix(read):
    n = len(read)
    if n == 0:
        return 0
    end_suffix = n - 1
    end_prefix = n // 2 - 1
    while end_prefix >= 0:
        if read[end_prefix] != read[end_suffix]:
            if end_suffix != n - 1:
                end_suffix = n - 1
            else:
                end_prefix -= 1
        else:
            end_suffix -= 1
            end_prefix -= 1
    return n - end_suffix - 1


# returns section len - read_size - letters_amount
def get_section_size(strand_section_len_before, frequency, read_size, letters_amount):
    classify_meta_data_len = int((strand_section_len_before // frequency) * letters_amount)

    if strand_section_len_before % frequency != 0:
        classify_meta_data_len += letters_amount

    return int(strand_section_len_before + classify_meta_data_len + read_size)


def create_padding(read_size, g_freq):
    return "A" * (g_freq - 1) + "G" + "A" * (read_size - 2 * g_freq) + "G" + "A" * (g_freq - 1)
