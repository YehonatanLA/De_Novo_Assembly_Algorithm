import Utilities_Test as ut
from Basic_Algorithm import algorithm
from Parallel_Algorithm.classify_strand_sections import classify_strand
from Parallel_Algorithm.classifying_no_parallel import final_algorithm
import time
from test_time import algorithm_basic

NUM_TESTS = 50


def run_iterative_algorithm(strand_size, read_size, real_edge_len, freq, letters_amount, classifications, g_freq,
                            sections_num, strand=""):
    if strand == "":
        original_strand = ut.generate_strand(strand_size)
    else:
        original_strand = strand

    classified_strand = classify_strand(original_strand, sections_num, freq, classifications, g_freq, read_size)
    # full cover
    parallel_algorithm_reads = ut.generate_reads(classified_strand, len(classified_strand), read_size)

    parallel_time = time.time()
    parallel_strand = final_algorithm(sections_num, letters_amount, classifications, real_edge_len, freq, strand_size,
                                      g_freq, read_size, parallel_algorithm_reads)
    parallel_time = time.time() - parallel_time
    parallel_algorithm_success = parallel_strand is not None and original_strand == parallel_strand
    return parallel_algorithm_success, parallel_time


def algorithm_ten_sections(strand_size):
    sections_num = 10
    total_successes = 0
    total_time = 0
    read_size = 200
    real_edge_len = 20
    freq = 10
    letters_amount = 2
    classifications = ut.create_classification(sections_num, letters_amount)
    g_freq = 25
    i = 0

    for _ in range(NUM_TESTS):
        i += 1
        print(f"test num {i}")
        success, time_of_algorithm = run_iterative_algorithm(strand_size, read_size, real_edge_len, freq,
                                                             letters_amount,
                                                             classifications, g_freq, sections_num)

        print(success)
        print(time_of_algorithm)
        if success is not None:
            total_successes += success
        total_time += time_of_algorithm

    success_rate = (total_successes / NUM_TESTS) * 100
    avg_time = total_time / NUM_TESTS

    return success_rate, avg_time


algorithm_ten_sections(10 ** 6)
