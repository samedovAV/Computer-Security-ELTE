# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(L):
    # Use a breakpoint in the code line below to debug your script.
    chars = []
    for i in range(len(L) - 1):
        chars.append(chr(L[i]))

    joined = "".join(chars).lower()

    result = joined[2:10] * 2
    print(result == "tgbharjftgbharjf")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi([88, 85, 84, 71, 66, 72, 65, 82, 74, 70, 87, 70, 85, 68, 74, 84, 81, 87, 79, 82])

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
