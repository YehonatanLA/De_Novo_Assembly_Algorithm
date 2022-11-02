import random
import math
from Alex_Algorithm import *

REAL_LENGTH = 20
NUM_OF_TESTS = 1000
SECTIONS = 15


def create_parallel_tests(letters, length):
    strand_length = length
    read_size = 100
    tests = 11
    sum_time = 0
    reads_num = 0

    for test_num in range(1, tests):
        strand = generate_strand(letters, strand_length)
        strand_input = open(f"millions_test/test{test_num}/strand_parallel.txt", "w")
        strand_input.write(strand)
        strand_input.close()
        start_time = time.time()
        reads = generate_reads_with_sections(strand, strand_length, read_size)
        end_time = time.time()
        sum_time += end_time - start_time
        for section in reads:
            reads_num += len(section)

        for section_num in range(0, SECTIONS):
            reads_file = open(f"millions_test/test{test_num}/section{section_num + 1}.txt", "w")
            for read in reads[section_num]:
                reads_file.write(f"{read}\n")
            reads_file.close()

    stat_file = open(f"millions_test/generate_parallel_stats{length}.txt", "w")
    stat_file.write("average time:\n")
    stat_file.write(f"{sum_time / tests}\n")
    stat_file.write("average read amount:\n")
    stat_file.write(f"{reads_num / tests}\n")
    stat_file.close()


def create_regular_tests(letters, length):
    strand_length = length
    read_size = 100
    tests = 11
    sum_time = 0
    reads_num = 0

    for test_num in range(1, tests):
        strand = generate_strand(letters, strand_length)
        strand_input = open(f"millions_test/test{test_num}/strand_regular.txt", "w")
        strand_input.write(strand)
        strand_input.close()
        start_time = time.time()
        reads = generate_reads(strand, strand_length, read_size)
        end_time = time.time()
        sum_time += end_time - start_time
        for section in reads:
            reads_num += len(section)

        reads_file = open(f"millions_test/test{test_num}/reads.txt", "w")
        for read in reads:
            reads_file.write(f"{read}\n")
        reads_file.close()

    stat_file = open(f"millions_test/generate_regular_stats{length}.txt", "w")
    stat_file.write("average time:\n")
    stat_file.write(f"{sum_time / tests}\n")
    stat_file.write("average read amount:\n")
    stat_file.write(f"{reads_num / tests}\n")
    stat_file.close()


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


def main():
    letters = ['A', 'C', 'G', 'T']

    create_regular_tests(letters, 1000000)
    create_parallel_tests(letters, 1000000)


if __name__ == "__main__":
    main()