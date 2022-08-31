import random
from tests import *

NUM_OF_TESTS = 1000
STRAND_LENGTH = 10000
WINDOW_SIZE = 50
REAL_LENGTH = 20
MAX_READ_AMOUNT = 10000


def generate_strand(letters):
    strand = ""
    for _ in range(0, STRAND_LENGTH):
        new_letter = random.choice(letters)
        strand = "".join([strand, new_letter])
    return strand
  

def generate_k_reads(strand, k):
    unused_letters = STRAND_LENGTH
    unused_arr = [False] * STRAND_LENGTH
    reads_starts = [False] * (STRAND_LENGTH - WINDOW_SIZE + 1)
    reads = []

    while k > 0:
        window_start = random.randint(0, STRAND_LENGTH - WINDOW_SIZE)
        if reads_starts[window_start]:
            continue
        reads_starts[window_start] = True
        k -= 1
        reads.append(strand[window_start:window_start + WINDOW_SIZE])

        for j in range(window_start, window_start + WINDOW_SIZE):
            if not unused_arr[j]:
                unused_letters -= 1
                unused_arr[j] = True

    return reads, unused_letters


def main():
    letters = ['A', 'C', 'G', 'T']
    strand = generate_strand(letters)
    print(f"strand: {strand}")

    for k in range(200, MAX_READ_AMOUNT, 100):
        success_amount = 0
        no_cover_counter = 0

        for _ in range(0, NUM_OF_TESTS):
            reads, unused_letters = generate_k_reads(strand, k)
            if unused_letters > 0:
                no_cover_counter += 1
                continue
            success_amount += final_algorithm(STRAND_LENGTH, WINDOW_SIZE, REAL_LENGTH, k, strand, reads)

        input_file = open(f"inputs/input{k}.txt", "w")
        input_file.write(f"{k}\n")
        input_file.write(f"{no_cover_counter}\n")
        input_file.write(f"{success_amount / NUM_OF_TESTS}\n")
        if NUM_OF_TESTS - no_cover_counter != 0:
            input_file.write(str(success_amount / (NUM_OF_TESTS - no_cover_counter)))
        else:
            input_file.write(str(0.0))
        input_file.close()


if __name__ == "__main__":
    main()
