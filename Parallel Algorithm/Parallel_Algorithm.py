import time
from multiprocessing import Process, Manager
from main import final_algorithm

from generate_reads import generate_strand, generate_reads
from classify_strand_sections import classify_sections
from declassify_reads import declassify_reads


def run_section_algorithm(section_reads_lst: list, section_len, read_size, real_edge_length,
                          complete_sections_dict, section):
    candidate_results = final_algorithm(section_len, read_size, real_edge_length, section_reads_lst)
    if type(candidate_results) is None or  len(candidate_results) != 1:
        # TODO: maybe figure out a way to solve cases like this?
        print("Algorithm failed - exiting...")
        exit(1)
    else:
        complete_sections_dict[section] = candidate_results[0]


def run_parallel_algorithm(reads_lst, read_size, real_edge_length, special_sections_length, letters_amount):
    """

    :param reads_lst: Each item of the list is a list of reads that is classified by a section
    :param read_size: The size of a read
    :param real_edge_length: A parameter for the original algorithm
    :param special_sections_length: The length of the first/last sections including classifications.
           In order to get the other sections' lengths, add read_size - letters_amount to this
    :param letters_amount: Amount of letters used for classifying the string to sections
    :return: If successful, then a list containing the sections of the original string, otherwise the list will have
             Nones in it which will indicate that the algorithm failed in at least one of the parallel sections
    """
    processes = []
    section_amount = len(reads_lst)
    manager = Manager()
    shared_dict = manager.dict()
    complete_sections = []

    for section in range(section_amount):
        # for section in range(2, 3):
        if 0 < section < section_amount - 1:
            section_len = special_sections_length + read_size - letters_amount

        else:
            section_len = special_sections_length

        p = Process(target=run_section_algorithm,
                    args=(reads_lst[section], int(section_len), read_size, real_edge_length, shared_dict,
                          section))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()

    for section_num in range(section_amount):
        complete_sections.append(shared_dict[section_num])
    return complete_sections


def main():
    test_num = 10
    letters = ['A', 'C', 'G', 'T']
    # classify = ["AC", "AG", "AT", "CA", "CC", "CG", "CT", "GA", "GC", "GG", "GT", "TA", "TC", "TG", "TT"]
    # classify = ["AC", "AG", "AT", "CA", "CC", "CG", "CT"]
    classify = ['AAC', 'AAG', 'AAT', 'ACA', 'ACC', 'ACG', 'ACT', 'AGA', 'AGC', 'AGG', 'AGT', 'ATA', 'ATC', 'ATG', 'ATT',
                'CAA', 'CAC', 'CAG', 'CAT', 'CCA', 'CCC', 'CCG', 'CCT', 'CGA', 'CGC', 'CGG', 'CGT', 'CTA', 'CTC', 'CTG',
                'CTT', 'GAA', 'GAC', 'GAG', 'GAT', 'GCA', 'GCC', 'GCG', 'GCT', 'GGA', 'GGC', 'GGG', 'GGT', 'GTA', 'GTC',
                'GTG', 'GTT', 'TAA', 'TAC', 'TAG']
    sections = 50
    read_size = 200
    letters_amount = 3
    real_edge_length = 20
    frequency = 15
    strand_len = 1000000
    g_freq = 25
    time_of_all_tests = 0
    padding = "A" * (g_freq - 1) + "G" + "A" * (read_size - 2 * g_freq) + "G" + "A" * (g_freq - 1)
    strand_section_len_before = strand_len / sections
    special_section_length = int(strand_section_len_before + int(strand_section_len_before * letters_amount / frequency) \
                                 + read_size + letters_amount)
    for i in range(test_num):
        print(f"Starting test {i}")
        generate_strand_start = time.time()
        strand_before = generate_strand(letters, strand_len)
        generate_strand_time = time.time() - generate_strand_start
        print("Generated strand")
        classify_sections_start = time.time()
        strand = classify_sections(strand_before, sections, frequency, classify, padding)
        classify_sections_time = time.time() - classify_sections_start
        print(f"strand length: {len(strand)}")
        print("Classified strand")
        generate_reads_start = time.time()
        dict_reads = generate_reads(strand, len(strand), read_size)
        generate_reads_time = time.time() - generate_reads_start
        print(f"Generated reads. There are {len(dict_reads)} reads.")
        declassify_reads_start = time.time()
        reads_by_sections = declassify_reads(dict_reads, sections, letters_amount, frequency, g_freq, classify, padding)
        declassify_reads_time = time.time() - declassify_reads_start
        print("Declassified reads")
        run_parallel_algorithm_start = time.time()
        complete_sections = run_parallel_algorithm(reads_by_sections, read_size, real_edge_length, special_section_length,
                                                   letters_amount)
        run_parallel_algorithm_time = time.time() - run_parallel_algorithm_start
        sum_time = declassify_reads_time + run_parallel_algorithm_time
        time_of_all_tests += sum_time
        print("finished parallel algorithm")

        if len(complete_sections) != sections:
            print(f"In test {i}, not all sections produced string!")
        else:
            print(f"In test {i}, there were {sections} strings from the algorithm!")
        print(
            f"Time to declassify reads: {declassify_reads_time}. percent of all time: "
            f"{(declassify_reads_time / sum_time) * 100}")
        print(
            f"Time to run parallel algorithm: {run_parallel_algorithm_time}. percent of all time: "
            f"{(run_parallel_algorithm_time / sum_time) * 100}")
        print(f"Time it took for the whole thing: {sum_time}")
    print(f"Average time it took to complete algorithm: {time_of_all_tests / test_num}")

    # generate_non_time = time.time()
    # reads_non_parallel = generate_reads(strand_before, len(strand_before), read_size)
    # generate_non_time = time.time() - generate_non_time
    # run_non_parallel_time = time.time()
    # # final_algorithm(len(strand_before), read_size, real_edge_length, reads_non_parallel)
    # run_non_parallel_time = time.time() - run_non_parallel_time
    # non_parallel_time_sum = run_non_parallel_time + generate_non_time

    # print(
    #     f"Time to generate_strand: {generate_strand_time}. percent of all time: "
    #     f"{(generate_strand_time / sum_time) * 100}")
    # print(
    #     f"Time to classify strand: {classify_sections_time}. percent of all time: "
    #     f"{(classify_sections_time / sum_time) * 100}")
    # print(
    #     f"Time to generate reads: {generate_reads_time}. percent of all time: {(generate_reads_time / sum_time) * 100}")

    # print(f"\nTime to run non parallel algorithm: {run_non_parallel_time}.")


if __name__ == "__main__":
    main()
