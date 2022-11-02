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

# the function returns the length of prefix that also a suffix in read
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


def compare_reads(prefix, suffix, suffix_start, len_match):
    for i in range(len_match):
        if prefix[i] != suffix[suffix_start + i]:
            return False
    return True

# returns section len - read_size - letters_amount
def get_section_size(strand_section_len_before, frequency, read_size, letters_amount):
    classify_meta_data_len = int((strand_section_len_before // frequency) * letters_amount)

    if strand_section_len_before % frequency != 0:
        classify_meta_data_len += letters_amount

    return int(strand_section_len_before + classify_meta_data_len + read_size)


def create_padding(read_size, g_freq):
    return "A" * (g_freq - 1) + "G" + "A" * (read_size - 2 * g_freq) + "G" + "A" * (g_freq - 1)
