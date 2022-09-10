import math
import textwrap


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
    :param read_size: how big will the read_size be
    :param frequency: how often to insert classifications of section in data
    :return: The new strand with both ways of meta-data included
    """
    # TODO: need to optimize for uneven division of sections_amount by strand length, last section will be shorter
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


def input_test_data():
    file_path_strand = input("Enter file path to strand:\n")
    file_path_classifications = input("Enter file path to classifications:\n")
    file_path_padding = input("Enter file path to padding:\n")
    file_path_sections = input("Enter file path to section amount:\n")
    file_path_read_size = input("Enter file path to read size:\n")
    file_path_frequency = input("Enter file path to frequency:\n")
    # the classifications for the tests we need is down below, but to be generic for different classifications I'll
    # put an option for input from files
    # classifications = ["AA", "AC", "AG", "AT", "CA", "CC", "CG", "CT", "GA", "GC", "GG", "GT", "TA", "TC", "TG", "TT"]

    file_strand = open(file_path_strand, "r")
    strand = file_strand.read().strip()
    file_classifications = open(file_path_classifications, "r")
    classifications = file_classifications.read().strip()
    file_padding = open(file_path_padding, "r")
    padding = file_padding.read().strip()
    file_sections = open(file_path_sections, "r")
    sections_amount = int(file_sections.read().strip())
    file_read_size = open(file_path_read_size, "r")
    read_size = int(file_read_size.read().strip())
    file_frequency = open(file_path_frequency, "r")
    frequency = int(file_frequency.read().strip())
    return strand, classifications, padding, sections_amount, read_size, frequency


def main():
    # you can change the inputs to fit from one file, or have multiple datas from same file
    # (for instance 5 different frequencies for different tests) you can change the code slightly for it in minutes.
    strand, classifications, padding, sections_amount, read_size, frequency = input_test_data()
    new_strand = classify_sections(strand, sections_amount, frequency, classifications, padding)
    # TODO: create function that saves the hash of 100 first letters of every section and stores it in a file
    print(new_strand)


if __name__ == "__main__":
    main()
