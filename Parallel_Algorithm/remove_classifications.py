from Parallel_Algorithm.classify_strand_sections import *


def remove_padding(sections_amount, strings_list, letters_amount, read_size):
    for section_num in range(sections_amount):
        if section_num == 0:
            strings_list[section_num] = strings_list[section_num][: -(read_size - letters_amount)]

        elif section_num == sections_amount - 1:
            strings_list[section_num] = strings_list[section_num][read_size - letters_amount:]
        else:
            strings_list[section_num] = strings_list[section_num][
                                        read_size - letters_amount: -(read_size - letters_amount)]
    return strings_list


def remove_classifications(sections_amount, strings_list, frequency, letters_amount):
    sections = []
    for section_num in range(sections_amount):
        sub_sections = textwrap.wrap(strings_list[section_num], width=frequency + letters_amount, break_long_words=True)
        section = "".join(sub_section[letters_amount:] for sub_section in sub_sections)
        if len(sub_sections[-1]) != letters_amount:
            sections.append(section[:-letters_amount])
        else:
            sections.append(section)

    strand_rebuilt = "".join(sections)
    return strand_rebuilt


def remove_meta_data(sections_amount, strings_list, frequency, letters_amount, read_size):
    strings_list = remove_padding(sections_amount, strings_list, letters_amount, read_size)
    return remove_classifications(sections_amount, strings_list, frequency, letters_amount)
