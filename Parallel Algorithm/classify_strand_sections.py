import math
import random
import textwrap
from generate_reads import generate_strand


def classify_sections(strand, sections_amount, frequency, classifications, padding):
    """
    The function recieves a strand and adds meta-data in order to classify each section of the strand.
    This is done by two ways:
     1) Every "frequency" amount of letters a classification of the section is added to the data.
        For example, frequency=3, strand=AGCTACGTACGTA and classification of "GG" will lead to
        AGGGCTGGACGGGTGGTAGGCGGGTAGG
     2) Between every section a padding of "read_size" length is added to the strand so a read
        will have only exactly one section of data.
    :param classifications: The different classifications in order for the sections
    :param padding: The padding to put between every section
    :param strand: the original strand without classification
    :param sections_amount: how many sections to divide the strand
    :param frequency: how often to insert classifications of section in data
    :return: The new strand with both ways of meta-data included
    """
    # TODO: adapt for uneven division of sections_amount by strand length, last section will be shorter
    sections_list = textwrap.wrap(strand, width=int(math.ceil(len(strand) / sections_amount)), break_long_words=True)

    for section_num in range(0, sections_amount):
        sub_sections = textwrap.wrap(sections_list[section_num], width=frequency, break_long_words=True)
        section_without_first_classification = \
            "".join(sub_section + classifications[section_num] for sub_section in sub_sections)

        if section_num != 0:
            section = "".join((padding, classifications[section_num], section_without_first_classification))
        else:
            section = "".join((classifications[section_num], section_without_first_classification))
        sections_list[section_num] = section

    return "".join(sections_list)


def generate_reads2(strand, num_of_reads, num_of_sections, read_len, strand_section_len_before, letters_amount, freq):
    dict_reads = dict()

    section_length = strand_section_len_before + strand_section_len_before * letters_amount / freq \
                     + read_len + letters_amount
    padding_starts = [int(i) for j in range(1, num_of_sections) for i in
                      range(int(j * section_length - read_len + 1), int(j * section_length))]

    for _ in range(num_of_reads):
        start_index = random.randint(0, len(strand) - read_len)
        read = strand[start_index:start_index + read_len]
        section = math.floor(start_index / section_length)
        if start_index in padding_starts:
            section += 1
        dict_reads[read] = section

    return dict_reads


def main():
    strand_len = 150000
    letters = ['A', 'C', 'G', 'T']
    strand = generate_strand(letters, strand_len)
    # print("Before:")
    # print(strand)

    # classifications = ["AC", "AG", "AT", "CA", "CC", "CG", "CT", "GA", "GC", "GG", "GT", "TA", "TC", "TG", "TT"]
    classifications = ["AT"]
    padding = "A" * 19 + "G" + "A" * 110 + "G" + "A" * 19
    sections_amount = 15
    frequency = 10
    new_strand = classify_sections(strand, sections_amount, frequency, classifications, padding)
    # print("After:")
    # print(new_strand)


if __name__ == "__main__":
    main()
