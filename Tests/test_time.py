import Utilities_Test as ut
from Basic_Algorithm import algorithm
from Parallel_Algorithm.classify_strand_sections import classify_strand
from Parallel_Algorithm.Parallel_Algorithm import final_algorithm
import time

NUM_TESTS = 10


def run_non_parallel_algorithm(strand_size, read_size, real_edge_len, strand=""):
    if strand == "":
        original_strand = ut.generate_strand(strand_size)
    else:
        original_strand = strand
    # full cover
    regular_algorithm_reads = ut.generate_reads(original_strand, strand_size, read_size)

    non_parallel_time = time.time()
    regular_algorithm_success = algorithm.final_algorithm(strand_size, read_size, real_edge_len, original_strand,
                                                          regular_algorithm_reads)
    non_parallel_time = time.time() - non_parallel_time
    return regular_algorithm_success, non_parallel_time


def run_parallel_algorithm(strand_size, read_size, real_edge_len, freq, letters_amount, classifications, g_freq,
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


def algorithm_basic(strand_size):
    total_successes = 0
    total_time = 0
    read_size = 200
    real_edge_len = 20
    i = 0

    for _ in range(NUM_TESTS):
        i += 1
        print(f"test num {i}")
        success, time_of_algorithm = run_non_parallel_algorithm(strand_size, read_size, real_edge_len)
        total_successes += success
        total_time += time_of_algorithm

    success_rate = (total_successes / NUM_TESTS) * 100
    avg_time = total_time / NUM_TESTS

    return success_rate, avg_time


def algorithm_ten_sections(strand_size):
    if strand_size == 1000000:
        return None, None
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
        success, time_of_algorithm = run_parallel_algorithm(strand_size, read_size, real_edge_len, freq, letters_amount,
                                                            classifications, g_freq, sections_num)
        if success is not None:
            total_successes += success
        total_time += time_of_algorithm

    success_rate = (total_successes / NUM_TESTS) * 100
    avg_time = total_time / NUM_TESTS

    return success_rate, avg_time


def algorithm_twenty_sections(strand_size):
    sections_num = 20
    total_successes = 0
    total_time = 0
    read_size = 200
    real_edge_len = 20
    freq = 10
    letters_amount = 3
    classifications = ut.create_classification(sections_num, letters_amount)
    g_freq = 25
    i = 0

    for _ in range(NUM_TESTS):
        i += 1
        print(f"test num {i}")
        success, time_of_algorithm = run_parallel_algorithm(strand_size, read_size, real_edge_len, freq, letters_amount,
                                                            classifications, g_freq, sections_num)
        total_successes += success
        total_time += time_of_algorithm

    success_rate = (total_successes / NUM_TESTS) * 100
    avg_time = total_time / NUM_TESTS

    return success_rate, avg_time


def algorithm_fifty_sections(strand_size):
    if strand_size < 1500000:
        return None, None

    sections_num = 50
    total_successes = 0
    total_time = 0
    read_size = 200
    real_edge_len = 20
    freq = 10
    letters_amount = 3
    classifications = ut.create_classification(sections_num, letters_amount)
    g_freq = 25
    i = 0

    for _ in range(NUM_TESTS):
        i += 1
        print(f"test num {i}")
        success, time_of_algorithm = run_parallel_algorithm(strand_size, read_size, real_edge_len, freq, letters_amount,
                                                            classifications, g_freq, sections_num)
        total_successes += success
        total_time += time_of_algorithm

    success_rate = (total_successes / NUM_TESTS) * 100
    avg_time = total_time / NUM_TESTS

    return success_rate, avg_time


def algorithm_hundred_sections(strand_size):
    sections_num = 100
    total_successes = 0
    total_time = 0
    read_size = 200
    real_edge_len = 20
    freq = 10
    letters_amount = 4
    classifications = ut.create_classification(sections_num, letters_amount)
    g_freq = 25
    i = 0

    for _ in range(NUM_TESTS):
        i += 1
        print(f"test num {i}")
        success, time_of_algorithm = run_parallel_algorithm(strand_size, read_size, real_edge_len, freq, letters_amount,
                                                            classifications, g_freq, sections_num)
        total_successes += success
        total_time += time_of_algorithm

    success_rate = (total_successes / NUM_TESTS) * 100
    avg_time = total_time / NUM_TESTS

    return success_rate, avg_time


def algorithm_five_hundred_sections(strand_size):
    if strand_size < 1000000:
        return None, None
    sections_num = 500
    total_successes = 0
    total_time = 0
    read_size = 200
    real_edge_len = 20
    freq = 10
    letters_amount = 5
    classifications = ut.create_classification(sections_num, letters_amount)
    g_freq = 25
    i = 0

    for _ in range(NUM_TESTS):
        i += 1
        print(f"test num {i}")
        success, time_of_algorithm = run_parallel_algorithm(strand_size, read_size, real_edge_len, freq, letters_amount,
                                                            classifications, g_freq, sections_num)
        total_successes += success
        total_time += time_of_algorithm

    success_rate = (total_successes / NUM_TESTS) * 100
    avg_time = total_time / NUM_TESTS

    return success_rate, avg_time


# this is the main function it gets an algorithm that its only parameter is strand size
# returns success rate and avg time
# see basic algorithm for example
def general_test(algorithm_test, file_name):
    dict_data = {}

    for strand_len in range(250_000, 1_500_001, 250_000):
        print(f"length currently is {strand_len}")
        success_rate, avg_time = algorithm_test(strand_len)
        dict_data[strand_len] = (success_rate, avg_time)
        if success_rate is not None and avg_time is not None:
            save_data(file_name, dict_data)
        dict_data = {}

    return dict_data


def save_data(file_name, dict_data):
    file = open(file_name, "a")
    file.write("strand length \t\t success_rate \t\t average time\n\n")
    for strand_len, (success_rate, avg_time) in dict_data.items():
        file.write(f"{strand_len}\t\t\t\t\t{success_rate}\t\t\t\t\t{avg_time}\n")
    file.close()


if __name__ == "__main__":
    f = open("basic.txt", "w")
    f.write("strand length \t\t success_rate \t\t average time\n\n")
    f.close()
    print(f"running basic")
    general_test(algorithm_basic, "basic.txt")
    f = open("ten.txt", "w")
    f.write("strand length \t\t success_rate \t\t average time\n\n")
    f.close()
    print(f"running 10 sections")
    general_test(algorithm_ten_sections, "ten.txt")
    f = open("twenty.txt", "w")
    f.write("strand length \t\t success_rate \t\t average time\n\n")
    f.close()
    print(f"running 20 sections")
    general_test(algorithm_twenty_sections, "twenty.txt")
    # f = open("fifty.txt", "w")
    # f.write("strand length \t\t success_rate \t\t average time\n\n")
    # f.close()
    # print(f"running 50 sections")
    # general_test(algorithm_fifty_sections, "fifty.txt")
    # f = open("one_hundred", "w")
    # f.write("strand length \t\t success_rate \t\t average time\n\n")
    # f.close()
    # print(f"running 100 sections")
    # general_test(algorithm_hundred_sections, "one_hundred.txt")
    # f = open("five_hundred.txt", "w")
    # f.write("strand length \t\t success_rate \t\t average time\n\n")
    # f.close()
    # print(f"running 500 sections")
    # general_test(algorithm_five_hundred_sections, "five_hundred.txt")
