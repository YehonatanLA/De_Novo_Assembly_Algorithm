import random
import math

REAL_LENGTH = 20
NUM_OF_TESTS = 1000
SECTIONS = 15


def generate_strand(letters, strand_length):
    strand_parts = []
    strand = ""
    for i in range(0, strand_length):
        new_letter = random.choice(letters)
        if i % 100000 == 0:
            strand_parts.append(str(strand))
            strand = ""
        strand = "".join([strand, new_letter])
    return "".join(strand_parts) + strand


def generate_reads(strand, strand_length, read_size):
    unused_letters = strand_length
    unused_arr = [False] * strand_length
    reads_starts = [False] * (strand_length - read_size + 1)
    reads = []

    while unused_letters > 0:
        window_start = random.randint(0, strand_length - read_size)
        if reads_starts[window_start]:
            continue
        reads_starts[window_start] = True
        reads.append(strand[window_start:window_start + read_size])

        for j in range(window_start, window_start + read_size):
            if not unused_arr[j]:
                unused_letters -= 1
                unused_arr[j] = True

    return reads


def generate_reads_with_sections(strand, strand_length, read_size):
    section_length = strand_length / SECTIONS
    unused_letters = strand_length
    unused_arr = [False] * strand_length
    reads_starts = [False] * (strand_length - read_size + 1)
    reads = [[] for _ in range(0, SECTIONS)]

    while unused_letters > 0:
        window_start = random.randint(0, strand_length - read_size)

        if reads_starts[window_start]:
            continue
        section_num_first = math.floor(window_start / section_length)
        section_num_last = math.floor((window_start + read_size - 1) / section_length)

        if section_num_first != section_num_last:
            continue
        reads_starts[window_start] = True
        reads[section_num_first].append(strand[window_start:window_start + read_size])

        for j in range(window_start, window_start + read_size):
            if not unused_arr[j]:
                unused_letters -= 1
                unused_arr[j] = True

    return reads
