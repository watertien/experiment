#! bin/python3
# -*- encoding: utf8 -*-

import binascii

__author__ = 'Tian'


def hex2binary(fname, output):
    # convert hex data into 8-bits binary file in UTF8 encoding
    lines = []
    with open(fname, "rb") as f:
        lines = f.readlines()

    for i, j in enumerate(lines):
        # select columns containing data
        # remove whitespaces
        lines[i] = b"".join(j[11:58].split(b" "))
        # lines is a list of binary strings

    print(lines[:5])
    # print(len(lines[0]))  # out: 32
    binary_data = ["".join([bin(j)[2:].zfill(8) for j in binascii.unhexlify(i)]) for i in lines]

    with open(output, "w") as f:
        for i in binary_data:
            f.write(f"{i}\n")

    print("Done!")


def datacheck(f1, f2):
    # driver statements:
    # valid = datacheck("../data/receiver_binary.txt", "../data/transmitter_binary.txt")
    # print(valid)
    with open(f1, "r") as f1, open(f2, "r") as f2:
        for i, j in zip(f1.readlines(), f2.readlines()):
            if len(i) != len(j):
                return False
            else:
                return True


def errorcount(f1, f2):
    if datacheck(f1, f2):
        error_count = 0
        total_count = 0
        with open(f1, "r") as f1, open(f2, "r") as f2:
            for i, j in zip(f1.readlines(), f2.readlines()):
                for x, y in zip(i, j):
                    total_count += 2
                    if x != y:
                        error_count += 1
        return error_count/total_count
    else:
        print("Please input two file of equal size!\nExit...")
        return None


if __name__ == "__main__":
    error_ratio = errorcount("../data/receiver_binary.txt", "../data/transmitter_binary.txt")
    print(f"The wrong code ratio is {error_ratio:.4%}")
