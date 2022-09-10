def generate_reads(strand, strand_length, read_size):
    unused_letters = strand_length
    unused_arr = [False] * strand_length
    reads_starts = [False] * (strand_length - read_size + 1)
    reads = []

    while unused_letters > 0:
        window_start = random.randint(0, strand_length - read_size)
        if reads_starts[window_start]:
            continue
        reads_starts[window_start] = True
        reads.append(strand[window_start:window_start + read_size])

        for j in range(window_start, window_start + read_size):
            if not unused_arr[j]:
                unused_letters -= 1
                unused_arr[j] = True

    return reads
