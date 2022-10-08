import time
from classify_strand_sections import *
from Utilities import Position

FIND_REPETITION_TIME = 0
FIND_PADDING_AUX_TIME = 0
CLASSIFY_READ_OTHER = 0


def find_repetitive_letters(read, letters_amount, frequency):
    for i in range(0, frequency + letters_amount):
        candidate = read[i: i + letters_amount]
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
    padding_len = 0
    found_g = False
    padding_has_g = False
    counter_from_g = 0
    last_padding_g_pos = None

    for pos in range(starting_index, final_index, jump):
        if read[pos] == "A":
            # found g in one of freq letters ago
            if found_g:
                # found g exactly freq letters ago
                if counter_from_g == freq:
                    last_padding_g_pos = pos - freq * jump
                    padding_len += freq + 1
                    found_g = False
                    padding_has_g = True
                # g was found less than freq letters ago
                else:
                    counter_from_g += 1
                    continue
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
        padding_position = Position.END
        padding_len, found_g = find_padding_aux(read, freq, len(read) - 1, -1, -1, g_freq)

    if padding_len < freq:
        padding_position = Position.NONE

    return padding_position, padding_len, found_g


def declassify_read(read, letters_amount, frequency, g_freq, letters_to_section, padding):
    # TODO: maybe throw bad reads (mainly  padding) at reading reads phase
    # check if the read is just padding or padding with up to two letters of classification
    if read == padding:
        return -1, None
    for letters in letters_to_section.keys():
        if read == padding[letters_amount:] + letters or read == letters + padding[0:-letters_amount]:
            return -1, None

    padding_position, padding_len, found_g = find_padding(read, frequency, g_freq)

    if padding_len > g_freq and found_g:

        if padding_position == Position.START:
            candidate_letters = read[padding_len: padding_len + letters_amount]
        else:
            candidate_letters = read[-padding_len - letters_amount: -padding_len]

    elif g_freq > padding_len >= frequency or padding_len > g_freq and not found_g:
        if padding_position == Position.START:
            candidate_letters = find_repetitive_letters(read[padding_len - letters_amount:], letters_amount,
                                                        frequency)
        else:
            candidate_letters = find_repetitive_letters(read[0:len(read) + letters_amount - padding_len],
                                                        letters_amount, frequency)
    else:
        candidate_letters = find_repetitive_letters(read, letters_amount, frequency)

    if len(candidate_letters) < letters_amount:
        return -1, None
    return letters_to_section[candidate_letters], [padding_position]


def declassify_reads(reads: list, num_of_sections, letters_amount, frequency, g_freq, classifications, padding):
    reads_by_sections = [[] for _ in range(num_of_sections)]
    padding_positions_by_sections = [[] for _ in range(num_of_sections)]
    letters_to_section = {classifications[i]: i for i in range(0, len(classifications))}

    for read in reads:
        try:
            section, padding_position = declassify_read(read, letters_amount, frequency, g_freq, letters_to_section,
                                                        padding)

            if section != -1:
                reads_by_sections[section].append(read)
                padding_positions_by_sections[section].append(padding_position[0])
        except KeyError:
            print(read)
    # adding the reads with a lot of padding: the first and last add one, other sections add two
    reads_by_sections[0].append(classifications[0] + padding[0:-letters_amount])
    padding_positions_by_sections[0].append(Position.END)
    reads_by_sections[-1].append(padding[letters_amount:] + classifications[-1])
    padding_positions_by_sections[-1].append(Position.START)

    for i in range(1, num_of_sections):
        reads_by_sections[i].append(padding[letters_amount:] + classifications[i])
        padding_positions_by_sections[i].append(Position.START)
        reads_by_sections[i].append(classifications[i] + padding[0:-letters_amount])
        padding_positions_by_sections[i].append(Position.END)
    return reads_by_sections, padding_positions_by_sections


def test_section(section_len):
    strand_len = 300000
    letters = ['A', 'C', 'G', 'T']
    strand = generate_strand(letters, strand_len)
    classify = ["AC", "AG", "AT", "CA", "CC", "CG", "CT", "GA", "GC", "GG", "GT", "TA", "TC", "TG", "TT"]
    padding = "A" * 19 + "G" + "A" * 78 + "G" + "A" * 19
    strand = classify_sections(strand, 15, 10, classify, padding)
    for freq in range(0, len(strand), 12):
        print(strand[freq: freq + 12])
    return find_repetitive_letters(strand[section_len + 1 + 150:section_len + 150 + 1 + section_len], 2, 10)


def main():
    # print(test_section(10000))
    strand_len = 1500000
    reads_amount = 1400000
    sections = 15
    read_size = 150
    bad_counter = 0
    letters_amount = 2
    frequency = 10
    letters = ['A', 'C', 'G', 'T']
    strand_before = generate_strand(letters, strand_len)
    print("Finished generating strand")
    strand_section_before_len = int(len(strand_before) / sections)
    classify = ["AC", "AG", "AT", "CA", "CC", "CG", "CT", "GA", "GC", "GG", "GT", "TA", "TC", "TG", "TT"]
    padding = "A" * 19 + "G" + "A" * 110 + "G" + "A" * 19
    strand = classify_sections(strand_before, sections, frequency, classify, padding)
    print("Finished classifying the strand")
    dict_reads = generate_reads2(strand, reads_amount, sections, read_size, strand_section_before_len, letters_amount,
                                 frequency)
    # for key, value in dict_reads.items():
    #     if key.find(classify[value]) >= 10:
    #         print(key.find(classify[value]))
    start_time = time.time()
    test_read_section = declassify_reads(dict_reads.keys(), sections, letters_amount, frequency, 20, classify, padding)
    end_time = time.time()
    print("Finished declassifying strand")
    # for section in range(15):
    #     for read in test_read_section[section]:
    #         if dict_reads[read] != section:
    #             bad_counter += 1
    # print(f"There were {bad_counter} bad declassified reads")
    print(f"Total time to take the declassifying for {reads_amount} reads is {end_time - start_time}")
    print(f"Of that time, it took overall {FIND_REPETITION_TIME} time for repetition func,"
          f" and {FIND_PADDING_AUX_TIME} for aux padding")
    print(f"Total time for other stuff is: {CLASSIFY_READ_OTHER}")
    #
    # letters_to_sections = {letters[i]: i for i in range(0, len(letters))}
    # section_to_letters = {i: letters[i] for i in range(0, len(letters))}
    # read = "AC" + "A" * 19 + "GA"
    # padding_position, padding_len = find_padding(read, 10, 20)
    # print(padding_position)
    # print(padding_len)


if __name__ == "__main__":
    main()
