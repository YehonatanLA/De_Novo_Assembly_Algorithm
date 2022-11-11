import random
from itertools import product

letters = ['A', 'C', 'G', 'T']


def generate_strand(strand_length):
    sub_strand = ""
    strand_parts = []
    i = 1

    for _ in range(0, strand_length):
        new_letter = random.choice(letters)
        sub_strand = "".join([sub_strand, new_letter])

        if i % 100000 == 0:
            strand_parts.append(sub_strand)
            sub_strand = ""
        i += 1
    strand_parts.append(sub_strand)
    return "".join(strand_parts)


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


def create_classification(sections, letters_amount):
    letters_str = ''.join(letters)
    lst = [''.join(x) for x in product(letters_str, repeat=letters_amount)]
    lst.pop(0)
    return lst[0:sections]
