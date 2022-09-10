from main import final_algorithm
import sys


def main():
    test_num = int(sys.argv[1])
    section = int(sys.argv[2])
    section_length = int(sys.argv[3])
    read_size = int(sys.argv[4])
    real_len = 20
    strand_file = open(f"millions_test/test{test_num}/strand_parallel.txt", "r")
    strand = strand_file.read().strip()
    strand_file.close()
    sub_strand = strand[(section - 1) * section_length: section * section_length]
    reads = []
    section_file = open(f"millions_test/test{test_num}/section{section}.txt", "r")

    for line in section_file:
        reads.append(line.strip())
    section_file.close()
    success, string_list = final_algorithm(section_length, read_size, real_len, len(reads), sub_strand, reads)
    string_file = open(f"millions_test/test{test_num}/string_section/section{section}.txt", "w")

    if len(string_list) > 0:
        for string_candidate in string_list:
            string_file.write(string_candidate)

    string_file.close()


if __name__ == "__main__":
    main()
