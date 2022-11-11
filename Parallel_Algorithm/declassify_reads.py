# from Parallel_Algorithm.Utilities import Position
# from Parallel_Algorithm.Utilities import Position
from classify_strand_sections import classify_strand
from Utilities import Position
from Tests import Utilities_Test as ut
import random


def find_repetitive_letters(read, letters_amount, frequency, bad_read, classifications):
    for i in range(0, frequency + letters_amount):
        candidate = read[i: i + letters_amount]
        if candidate not in classifications:
            continue
        if candidate == bad_read:
            continue
        was_repetitive = True

        for j in range(i + frequency + letters_amount, len(read), frequency + letters_amount):
            temp = read[j:j + letters_amount]

            if len(temp) != len(candidate):
                break
            if temp != candidate:
                was_repetitive = False
                break

        if was_repetitive:
            return candidate
    return ""


def find_padding_aux(read, freq, starting_index, final_index, jump, g_freq):
    """
    How the function works:
    from the starting index until stopped or until the final index,
    the function iterates through the read and checks if the current letter is 'A'.
    If so, add 1 to counter and go to next letter.
    If there is a 'G', make sure it's part of the padding and if not, break.
    Otherwise, break.

    :param read: the read to be searched for padding
    :param freq: how often the classification letters appear in the strand
    :param starting_index: the index the function is starting to look for padding from
    :param final_index: the index the function is finishing looking for the padding
    :param jump: in what way to iterate through the read (1 or -1)
    :param g_freq: the index where a g appears first in the padding read from the start of padding
    :return: The function returns the true padding length inside the read
    if the padding is over g_freq + classification_letters_len,
    almost accurate padding otherwise

    """
    padding_len = 0
    found_g = False
    padding_has_g = False
    counter_from_g = 0
    last_padding_g_pos = None

    for pos in range(starting_index, final_index, jump):
        if found_g:
            # found g exactly freq letters ago
            if counter_from_g == g_freq:  # changed
                last_padding_g_pos = pos - g_freq * jump
                padding_len += g_freq
                found_g = False
                padding_has_g = True
            # g was found less than freq letters ago
            else:
                counter_from_g += 1
                continue

        if read[pos] == "A":
            # found g in one of freq letters ago
            padding_len += 1

        elif read[pos] == "G":
            if not found_g:
                found_g = True
                counter_from_g = 1
                continue
            else:
                break
        # either C or T were found, break automatically
        else:
            break

    if last_padding_g_pos is not None:
        padding_len = len(read[starting_index:last_padding_g_pos:jump]) + g_freq
    return padding_len, padding_has_g


def find_padding(read, freq, g_freq):
    padding_position = Position.START
    # start from beginning
    padding_len, found_g = find_padding_aux(read, freq, 0, len(read), 1, g_freq)

    if padding_len < freq:
        # start from end
        padding_position = Position.END
        padding_len, found_g = find_padding_aux(read, freq, len(read) - 1, -1, -1, g_freq)

    if padding_len < freq:
        padding_position = Position.NONE

    return padding_position, padding_len, found_g


def declassify_read(read, letters_amount, frequency, g_freq, letters_to_section, padding, bad_read, classifications):
    # too close to a full padding read, can't be used for declassification
    if read == padding:
        return -1, None

    padding_position, padding_len, found_g = find_padding(read, frequency, g_freq)

    if padding_len >= len(padding) - letters_amount:
        return -1, None

    # can accurately tell how much padding and that padding has g
    if padding_len > g_freq and found_g:

        if padding_position == Position.START:
            candidate_letters = read[padding_len: padding_len + letters_amount]
        else:
            candidate_letters = read[-padding_len - letters_amount: -padding_len]

    # padding exists without g (length is between freq and g_freq)
    # so it will find classification with high probability if tsome padding is removed
    elif g_freq > padding_len >= frequency or padding_len > g_freq and not found_g:

        if padding_position == Position.START:
            candidate_letters = find_repetitive_letters(read[padding_len - letters_amount:], letters_amount,
                                                        frequency, bad_read, classifications)
        else:
            candidate_letters = find_repetitive_letters(read[0:len(read) + letters_amount - padding_len],
                                                        letters_amount, frequency, bad_read, classifications)
    # no padding
    else:
        candidate_letters = find_repetitive_letters(read, letters_amount, frequency, bad_read, classifications)
        padding_position = Position.NONE

    if len(candidate_letters) < letters_amount:
        return -1, None
    return letters_to_section[candidate_letters], [padding_position]


def declassify_reads(reads: list, num_of_sections, letters_amount, frequency, g_freq, classifications, padding):
    bad_read = 'A' * letters_amount
    reads_by_sections = [[] for _ in range(num_of_sections)]
    paddings_by_sections = [[[], []] for _ in range(num_of_sections)]
    letters_to_section = {classifications[i]: i for i in range(0, len(classifications))}

    for read in reads:
        try:
            section, padding_position = declassify_read(read, letters_amount, frequency, g_freq, letters_to_section,
                                                        padding, bad_read, classifications)

            if section != -1:
                if padding_position[0] == Position.START:
                    paddings_by_sections[section][0].append(read)
                elif padding_position[0] == Position.END:
                    paddings_by_sections[section][1].append(read)
                reads_by_sections[section].append(read)

        except KeyError:
            print(read)
    # adding reads with a lot of padding: the first and last add one, other sections add two

    # reads_by_sections[0].append(classifications[0] + padding[0:-letters_amount])
    # paddings_by_sections[0][1].append(classifications[0] + padding[0:-letters_amount])
    # reads_by_sections[-1].append(padding[letters_amount:] + classifications[-1])
    # paddings_by_sections[-1][0].append(padding[letters_amount:] + classifications[-1])
    #
    # for i in range(1, num_of_sections - 1):
    #     paddings_by_sections[i][0].append(padding[letters_amount:] + classifications[i])
    #     reads_by_sections[i].append(padding[letters_amount:] + classifications[i])
    #     paddings_by_sections[i][1].append(classifications[i] + padding[0:-letters_amount])
    #     reads_by_sections[i].append(classifications[i] + padding[0:-letters_amount])
    return reads_by_sections, paddings_by_sections


def main():
    # read = "AAAAAAAAAAAAAAAAAAAAAAAGAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAGAAAAAAAAAAAAAAAAAAAAAAAAG"
    # letters_amount = 2
    # frequency = 10
    # g_freq = 25
    # bad_read = letters_amount * "A"
    # classifications = ut.create_classification(10, letters_amount)
    # letters_to_section = {classifications[i]: i for i in range(0, len(classifications))}
    # print(declassify_read(read, letters_amount, frequency, g_freq, letters_to_section, padding, bad_read,
    #                       classifications))
    padding = 24 * "A" + "G" + 150 * "A" + "G" + 24 * "A"
    section_amount = 10
    letters_amount = 2
    frequency = 10
    read_size = 200
    g_freq = 25
    strand_length = 500000
    classifications = ut.create_classification(section_amount, letters_amount)
    strand = ut.generate_strand(strand_length)
    classified_strand = classify_strand(strand, section_amount, frequency, classifications, g_freq, read_size)
    dict_reads = generate_reads_2(classified_strand, read_size, strand, section_amount, frequency, letters_amount)
    reads_by_sections, padding_by_sections = declassify_reads(list(dict_reads.keys()), section_amount, letters_amount, frequency, g_freq, classifications, paddding)

    for section in reads_by_sections:
        for read in section:
            if dict_reads[read] != section:
                print("Mismatch:")
                print(f"read: {read}")
                print(f"we declassified as section {section}")
                print(f"the test showed section {dict_reads[read]}\n")

letters = ['A', 'C', 'G', 'T']


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


if __name__ == '__main__':
    main()
