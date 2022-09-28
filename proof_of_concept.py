import random

letters = ['A', 'C', 'G', 'T']


def generate_strand(strand_len):
    return ''.join(random.choice(letters) for _ in range(strand_len))


def generate_reads_(meta_data_strand, num_of_reads, read_size, strand_no_meta_data_len, section_amount, freq,
                    letters_amount):
    """
    :param meta_data_strand: strand with the mata data
    :param strand_no_meta_data_len: the len of the original strand with no meta-data
    :return: dict:  key is a read, value is a section
    """
    dict_reads = dict()
    g = int(((strand_no_meta_data_len / section_amount) * (1 + (letters_amount / freq))) + letters_amount)
    section_indexes = [[] for _ in range(section_amount)]
    section_indexes[0] = (0, g - 2)
    for i in range(1, section_amount):
        element = section_indexes[i - 1]
        new_tup = (element[1] + 4, element[1] + g + read_size)
        section_indexes[i] = new_tup

    for _ in range(num_of_reads):
        start_index = random.randint(0, len(meta_data_strand) - read_size)
        read = meta_data_strand[start_index:start_index + read_size]
        section = -1
        for i in range(section_amount):
            if start_index >= section_indexes[i][0] and start_index <= section_indexes[i][1]:
                section = i
        if section != -1:
            dict_reads[read] = section
    return dict_reads


# generate all the possible reads, the amount of reads is (length_meta_data_strand - read size)
def generate_reads_2(meta_data_strand, read_size, strand_no_meta_data_len, section_amount, freq,
                     letters_amount):
    """
    :param meta_data_strand: strand with the mata data
    :param strand_no_meta_data_len: the len of the original strand with no meta data
    :return: dict:  key is a read, value is a section
    """
    dict_reads = dict()
    g = int(((strand_no_meta_data_len / section_amount) * (1 + (letters_amount / freq))) + letters_amount)
    section_indexes = [[] for _ in range(section_amount)]
    section_indexes[0] = (0, g - 2)
    for i in range(1, section_amount):
        element = section_indexes[i - 1]
        new_tup = (element[1] + 4, element[1] + g + read_size)
        section_indexes[i] = new_tup

    for j in range(len(meta_data_strand) - read_size + 1):
        start_index = j
        read = meta_data_strand[start_index:start_index + read_size]
        section = -1
        for i in range(section_amount):
            cond1 = start_index >= section_indexes[i][0]
            cond2 = start_index <= section_indexes[i][1]
            if cond1 and cond2:
                section = i
        if section != -1:
            dict_reads[read] = section
    return dict_reads
