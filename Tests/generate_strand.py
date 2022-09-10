def generate_strand(letters, strand_length):
    strand = ""
    for _ in range(0, strand_length):
        new_letter = random.choice(letters)
        strand = "".join([strand, new_letter])
    return strand
