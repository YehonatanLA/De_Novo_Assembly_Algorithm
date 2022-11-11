import Utilities_Test as ut
from Basic_Algorithm import algorithm
from Parallel_Algorithm.classify_strand_sections import classify_strand
from Parallel_Algorithm.Parallel_Algorithm import final_algorithm
import math
from Parallel_Algorithm.declassify_reads import declassify_read

def run_test(strand_size, read_size, real_edge_len, freq, letters_amount, classifications, g_freq,
             sections_num, strand=""):
    if strand == "":
        original_strand = ut.generate_strand(strand_size)
    else:
        original_strand = strand
    regular_algorithm_reads = ut.generate_reads(original_strand, strand_size, read_size)
    regular_algorithm_success = algorithm.final_algorithm(strand_size, read_size, real_edge_len, original_strand,
                                                          regular_algorithm_reads)

    classified_strand = classify_strand(original_strand, sections_num, freq, classifications, g_freq, read_size)
    parallel_algorithm_reads = ut.generate_reads(classified_strand, len(classified_strand), read_size)
    parallel_strand = final_algorithm(sections_num, letters_amount, classifications, real_edge_len, freq, strand_size,
                                      g_freq, read_size, parallel_algorithm_reads)

    parallel_algorithm_success = parallel_strand and original_strand == parallel_strand

    return parallel_algorithm_success == regular_algorithm_success


def test_different_strand_sizes(read_size, real_edge_len, frequency, letters_amount, classifications, g_freq,
                                sections_num):
    test_num = 10
    success_counter = 0
    counter = 0

    for strand_size in range(150000, 1500001, 150000):
        for _ in range(test_num):
            counter += 1
            success_counter += run_test(strand_size, read_size, real_edge_len, frequency, letters_amount,
                                        classifications, g_freq, sections_num)

        success_rate = (success_counter / counter) * 100
        print(f"test_different_sizes test success rate: {success_rate}%")


def test_different_number_of_sections(strand_size, read_size, real_edge_len, frequency, g_freq):
    test_num = 10
    success_counter = 0
    counter = 0
    max_letters_amount = 6

    sections_amount = [10, 20, 30, 50, 100, 500]
    min_letters_amount_by_sections = [math.floor(math.log(x, 4)) + 1 for x in sections_amount]

    letters_amount_by_sections = []
    for i in range(len(min_letters_amount_by_sections)):
        new_lst = []
        for j in range(min_letters_amount_by_sections[i], max_letters_amount):
            new_lst.append(j)
        letters_amount_by_sections.append(new_lst)

    test_lst = []
    for i in range(len(sections_amount)):
        for j in range(len(letters_amount_by_sections[i])):
            test_lst.append((sections_amount[i], letters_amount_by_sections[i][j]))

    for (sections_amount, letters_amount) in test_lst:
        print(f"sections amount: {sections_amount}")
        for _ in range(test_num):
            counter += 1
            classifications = ut.create_classification(sections_amount, letters_amount)

            success_counter += run_test(strand_size, read_size, real_edge_len, frequency, letters_amount,
                                        classifications, g_freq, sections_amount)

    success_rate = (success_counter / counter) * 100
    print(f"test_different_number_of_sections success rate: {success_rate}%")


def test_one_strand(strand, read_size, real_edge_len, frequency, letters_amount, classifications, g_freq,
                    sections_num):
    test_num = 10
    success_counter = 0
    counter = 0
    for _ in range(test_num):
        success_counter += run_test(len(strand), read_size, real_edge_len, frequency, letters_amount, classifications,
                                    g_freq, sections_num, strand)
        counter += 1
    success_rate = (success_counter / counter) * 100
    print(f"test_one_strand success rate: {success_rate}%")


def main():
    strand_size_sanity = 150000
    sections_num = 15
    letters_amount = 2
    real_edge_len = 20
    frequency = 10
    g_freq = 25
    read_size = 150
    strand_size_sections_test = 100000
    classifications = ut.create_classification(sections_num, letters_amount)

    test_different_strand_sizes(read_size, real_edge_len, frequency, letters_amount, classifications, g_freq,
                                sections_num)
    test_different_number_of_sections(strand_size_sections_test, read_size, real_edge_len, frequency, g_freq)

    strand = ut.generate_strand(strand_size_sanity)
    test_one_strand(strand, read_size, real_edge_len, frequency, letters_amount, classifications, g_freq,
                    sections_num)


if __name__ == "__main__":
    # main()

    read = "AAAAAAAAAAAAAAAAAAAAAAAGAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAGAAAAAAAAAAAAAAAAAAAAAAAAG"
    letters_amount = 2
    frequency = 10
    g_freq = 25
    padding = 24 * "A" + "G" + 150 * "A" + "G" + 24 * "A"
    bad_read = letters_amount * "A"
    classifications = ut.create_classification(10, letters_amount)
    letters_to_section = {classifications[i]: i for i in range(0, len(classifications))}

    print(declassify_read(read, letters_amount, frequency, g_freq, letters_to_section, padding, bad_read, classifications))
