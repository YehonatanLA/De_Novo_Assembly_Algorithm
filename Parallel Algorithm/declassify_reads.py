from Utilities import Position


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
        # start from end
        padding_position = Position.END
        padding_len, found_g = find_padding_aux(read, freq, len(read) - 1, -1, -1, g_freq)

    if padding_len < freq:
        padding_position = Position.NONE

    return padding_position, padding_len, found_g


def declassify_read(read, letters_amount, frequency, g_freq, letters_to_section, padding):
    # too close to a full padding read, can't be used for declassification
    if read == padding:
        return -1, None
    for letters in letters_to_section.keys():
        if read == padding[letters_amount:] + letters or read == letters + padding[0:-letters_amount]:
            return -1, None

    padding_position, padding_len, found_g = find_padding(read, frequency, g_freq)

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
                                                        frequency)
        else:
            candidate_letters = find_repetitive_letters(read[0:len(read) + letters_amount - padding_len],
                                                        letters_amount, frequency)
    # no padding
    else:
        candidate_letters = find_repetitive_letters(read, letters_amount, frequency)
        padding_position = Position.NONE

    if len(candidate_letters) < letters_amount:
        return -1, None
    return letters_to_section[candidate_letters], [padding_position]


def declassify_reads(reads: list, num_of_sections, letters_amount, frequency, g_freq, classifications, padding):
    reads_by_sections = [[] for _ in range(num_of_sections)]
    paddings_by_sections = [[[], []] for _ in range(num_of_sections)]
    letters_to_section = {classifications[i]: i for i in range(0, len(classifications))}

    for read in reads:
        try:
            section, padding_position = declassify_read(read, letters_amount, frequency, g_freq, letters_to_section,
                                                        padding)

            if section != -1:
                if padding_position[0] == Position.START:
                    paddings_by_sections[section][0].append(read)
                elif padding_position[0] == Position.END:
                    paddings_by_sections[section][1].append(read)
                reads_by_sections[section].append(read)

        except KeyError:
            print(read)
    # adding reads with a lot of padding: the first and last add one, other sections add two
    reads_by_sections[0].append(classifications[0] + padding[0:-letters_amount])
    paddings_by_sections[0][1].append(classifications[0] + padding[0:-letters_amount])
    reads_by_sections[-1].append(padding[letters_amount:] + classifications[-1])
    paddings_by_sections[-1][0].append(padding[letters_amount:] + classifications[-1])

    for i in range(1, num_of_sections - 1):
        paddings_by_sections[i][0].append(padding[letters_amount:] + classifications[i])
        reads_by_sections[i].append(padding[letters_amount:] + classifications[i])
        paddings_by_sections[i][1].append(classifications[i] + padding[0:-letters_amount])
        reads_by_sections[i].append(classifications[i] + padding[0:-letters_amount])
    return reads_by_sections, paddings_by_sections
