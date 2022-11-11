import math
import textwrap
from Parallel_Algorithm.Utilities import create_padding

def classify_strand(strand, sections_amount, frequency, classifications, g_freq, read_size):
    """
    The function receives a strand and adds meta-data in order to classify each section of the strand.
    This is done by two ways:
     1) Every "frequency" amount of letters a classification of the section is added to the data.
        For example, frequency=3, strand=AGCTACGTACGTA and classification of "GG" will lead to
        AGGGCTGGACGGGTGGTAGGCGGGTAGG
     2) Between every section a padding of "read_size" length is added to the strand so a read
        will have only exactly one section of data.
    :param read_size: the length of a read when reading parts of the strand
    :param g_freq: the index of the leftmost 'G' in the padding (starting from 1)
    :param classifications: The different classifications in order for the sections
    :param padding: The padding to put between every section
    :param strand: the original strand without classification
    :param sections_amount: how many sections to divide the strand
    :param frequency: how often to insert classifications of section in data
    :return: The new strand with both ways of meta-data included
    """
    padding = create_padding(read_size, g_freq)
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
