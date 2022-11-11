def compare_strings(original, created):
    diff = False

    for i in range(len(original)):
        if original[i] != created[i]:
            print(f"They are different in index {i}.")
            print(f"The strand is {original[i - 10: i + 10]}")
            print(f"The created is {original[i - 10: i + 10]}")
            diff = True
            break

    if not diff:
        print("Strings are identical!")
