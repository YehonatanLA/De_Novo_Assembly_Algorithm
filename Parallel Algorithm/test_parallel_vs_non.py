import subprocess
import threading
import os
from generate_reads import *

SECTIONS = 16
READ_SIZE = 100


def run_section(test_num, section, section_length):
    subprocess.call(["python", "parallel_script.pyw", str(test_num), str(section), str(section_length), str(READ_SIZE)])


def test_no_parallel(strand, test_num, length):
    real_len = 20
    print(f"No parallel test number {test_num}")
    reads = []
    reads_file = open(f"millions_test/test{test_num}/reads.txt", "r")

    for line in reads_file:
        reads.append(line.strip())

    reads_file.close()

    start_time = time.time()
    success, junk = final_algorithm(length, READ_SIZE, real_len, len(reads), strand, reads)
    end_time = time.time()
    return end_time - start_time, success


def find_real_str_with_backtrack(strand, candidate_strs, temp_str, section):
    if section == SECTIONS and temp_str == strand:
        return True

    elif section == SECTIONS:
        return False

    for candidate in candidate_strs[section]:
        temp_str += candidate
        if find_real_str_with_backtrack(strand, candidate_strs, temp_str, section + 1):
            return True
        temp_str = temp_str[0:len(temp_str) - len(candidate)]
    return False


def test_parallel(length):
    test_num = 11
    success_amount = 0
    sum_time_parallel = 0
    threads = []

    for j in range(1, test_num):
        print(f"Parallel test number {j}")
        strand_file = open(f"millions_test/test{j}/strand_parallel.txt", "r")
        strand = strand_file.read().strip()
        strand_file.close()
        start_time = time.time()

        for section in range(1, SECTIONS + 1):
            # running threads to rebuild parts of the string by sections and store it in files
            t = threading.Thread(target=run_section,
                                 args=(j, section, int(length / SECTIONS)), )
            t.start()
            threads.append(t)

        for t in threads:
            t.join()

        candidate_strs = [[] for _ in range(0, SECTIONS)]

        # reading the sub strings from files
        for section in range(1, SECTIONS + 1):
            file_path = f"millions_test/test{j}/string_section/section{section}.txt"
            if os.stat(file_path).st_size == 0:
                print(f'File millions_test/test{j}/string_section/section{section}.txt is empty'
                      f', algorithm failed!')
                exit(1)

            sub_string_file = open(file_path)

            for sub_string in sub_string_file:
                sub_string = sub_string.strip()
                candidate_strs[section - 1].append(sub_string)

            sub_string_file.close()

        # TODO: I sort of checked the backtracking function with some tests, but it might not be 100%
        #   please go over it to make sure it is ok
        #  (wrote it in 10 minutes just to run the code before I go to family)
        success = find_real_str_with_backtrack(strand, candidate_strs, "", 0)
        end_time = time.time()
        sum_time_parallel += end_time - start_time
        success_amount += success

    no_parallel_stats = open(f"millions_test/parallel_stats{length}.txt", "w")
    no_parallel_stats.write("Time for average test:\n")
    no_parallel_stats.write(f"{sum_time_parallel / (test_num - 1)}\n")
    no_parallel_stats.write("Success amount:\n")
    no_parallel_stats.write(f"{success_amount}\n")
    no_parallel_stats.close()


def main():
    # prerequisites for the test: need the following files/directories in the same directory as the one running main:
    # millions_test, millions_test/test{i} for i in 1,10 (or what you define)
    # millions_test/test{i}/string_section
    # some work, defining lengths to run tests and storing srand and reads for both parallel and non-parallel
    letters = ['A', 'C', 'G', 'T']
    lengths = [2, 5, 10, 20, 50, 100, 200, 500]

    for length in lengths:
        print(f"\n\ncurrent length: {length}")
        length *= 1000000
        create_regular_tests(letters, length)
        print("finished generating for regular")
        create_parallel_tests(letters, length)
        print("finished generating for parallel")
        test_num = 11
        success_amount = 0
        sum_time_no_parallel = 0

        for j in range(1, test_num):
            strand_file = open(f"millions_test/test{j}/strand_regular.txt", "r")
            strand = strand_file.read().strip()
            strand_file.close()

            # no parallel test
            temp_time, success = test_no_parallel(strand, j, length)
            sum_time_no_parallel += temp_time
            success_amount += success

        no_parallel_stats = open(f"millions_test/no_parallel_stats{length}.txt", "w")
        no_parallel_stats.write("Time for average test:\n")
        no_parallel_stats.write(f"{sum_time_no_parallel / (test_num - 1)}\n")
        no_parallel_stats.write("Success amount:\n")
        no_parallel_stats.write(f"{success_amount}\n")
        no_parallel_stats.close()

        # parallel test
        test_parallel(length)


if __name__ == "__main__":
    main()
