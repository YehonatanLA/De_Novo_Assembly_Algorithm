import math
from tests import *

REAL_LENGTH = 20
NUM_OF_TESTS = 1000


def test_different_strand_lengths(letters):
    read_size = 1000
    length = 100000
    test_type = "strand_length"
    count = 1
    test_num = 100
    print("started test_different_strand_lengths!")

    while length <= 1000000:
        print(f"test number {count}")
        directory = f"input{count}"
        strand = generate_strand(letters, length)
        do_test(strand, length, read_size, test_type, directory, test_num)
        length += 100000
        count += 1


def test_different_read_sizes(letters):
    strand_length = 10000
    read_size = 200
    test_type = "read_size"
    count = 4
    test_num = 1000
    strand = generate_strand(letters, strand_length)
    print("started test_different_read_sizes!")

    while read_size <= 500:
        print(f"test number {count}")
        directory = f"input{count}"
        do_test(strand, strand_length, read_size, test_type, directory, test_num)
        read_size += 50
        count += 1


def do_test(strand, strand_length, read_size, test_type, directory, test_num):
    for k in range(math.ceil(strand_length / read_size), strand_length - read_size + 1, read_size):
        success_amount = 0
        no_cover_counter = 0

        for _ in range(0, test_num):
            reads, unused_letters = generate_k_reads(strand, k, strand_length, read_size)
            if unused_letters > 0:
                no_cover_counter += 1
                continue
            success_amount += final_algorithm(strand_length, read_size, REAL_LENGTH, k, strand, reads)

        input_file = open(f"{test_type}/{directory}/test{k}.txt", "w")
        input_file.write(f"{k}\n")
        input_file.write(f"{no_cover_counter}\n")
        input_file.write(f"{success_amount / NUM_OF_TESTS}\n")
        if NUM_OF_TESTS - no_cover_counter != 0:
            input_file.write(str(success_amount / (NUM_OF_TESTS - no_cover_counter)))
        else:
            input_file.write(str(0.0))
        input_file.close()


def generate_strand(letters, strand_length):
    strand = ""
    for _ in range(0, strand_length):
        new_letter = random.choice(letters)
        strand = "".join([strand, new_letter])
    return strand


def generate_k_reads(strand, k, strand_length, read_size):
    unused_letters = strand_length
    unused_arr = [False] * strand_length
    reads_starts = [False] * (strand_length - read_size + 1)
    reads = []

    while k > 0:
        window_start = random.randint(0, strand_length - read_size)
        if reads_starts[window_start]:
            continue
        reads_starts[window_start] = True
        k -= 1
        reads.append(strand[window_start:window_start + read_size])

        for j in range(window_start, window_start + read_size):
            if not unused_arr[j]:
                unused_letters -= 1
                unused_arr[j] = True

    return reads, unused_letters


def main():
    letters = ['A', 'C', 'G', 'T']

    test_different_read_sizes(letters)
    test_different_strand_lengths(letters)


if __name__ == "__main__":
    main()
