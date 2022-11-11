from Parallel_Algorithm.Alex_Algorithm import alex_algorithm
from Parallel_Algorithm.Utilities import get_section_size, create_padding
from Parallel_Algorithm.declassify_reads import declassify_reads
from Parallel_Algorithm.remove_classifications import remove_meta_data

is_failed = -1


def run_section_algorithm(section_reads_lst: list, paddings_positions, section_len, read_size,
                          real_edge_length,
                          complete_sections_dict, section):
    candidate_results = alex_algorithm(section_len, read_size, real_edge_length, section_reads_lst,
                                       paddings_positions)

    if candidate_results is None or len(candidate_results) != 1:
        complete_sections_dict[is_failed] = 1

    else:
        complete_sections_dict[section] = candidate_results[0]


def run_parallel_algorithm(reads_lst, paddings_by_sections, read_size, real_edge_length,
                           special_sections_length, letters_amount):
    """
    :param paddings_by_sections: A list of sections, in each item has a list of padding position
           (weather starting at beginning of read, end of read or has no padding)
    :param reads_lst: Each item of the list is a list of reads that is classified by a section
    :param read_size: The size of a read
    :param real_edge_length: A parameter for the original algorithm
    :param special_sections_length: The length of the first/last sections including classifications.
           In order to get the other sections' lengths, add read_size - letters_amount to this
    :param letters_amount: Amount of letters used for classifying the string to sections
    :return: If successful, then a list containing the sections of the original string, otherwise the list will have
             Nones in it which will indicate that the algorithm failed in at least one of the parallel sections
    """
    section_amount = len(reads_lst)
    shared_dict = dict()
    complete_sections = []

    for section in range(section_amount):
        if 0 < section < section_amount - 1:
            section_len = special_sections_length + read_size - letters_amount

        else:
            section_len = special_sections_length

        run_section_algorithm(reads_lst[section], paddings_by_sections[section], int(section_len), read_size,
                              real_edge_length, shared_dict, section)

    if is_failed in shared_dict.keys():
        return None

    for section_num in range(section_amount):
        complete_sections.append(shared_dict[section_num])
    return complete_sections


def final_algorithm(sections_num, letters_amount, classify, real_edge_len, frequency, strand_len, g_freq, read_size,
                    read_lst):
    # declassify each read by its section
    padding = create_padding(read_size, g_freq)
    reads_by_sections, paddings_by_sections = declassify_reads(read_lst, sections_num, letters_amount, frequency,
                                                               g_freq, classify, padding)

    # run for each section Alex's algorithm
    strand_section_len_before = strand_len / sections_num
    special_section_length = get_section_size(strand_section_len_before, frequency, read_size, letters_amount)
    complete_sections = run_parallel_algorithm(reads_by_sections, paddings_by_sections, read_size,
                                               real_edge_len, special_section_length,
                                               letters_amount)

    if complete_sections is None:
        return None
    # remove metadata from the solution
    strand_rebuilt = remove_meta_data(sections_num, complete_sections, frequency, letters_amount, read_size)

    return strand_rebuilt