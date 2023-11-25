# !/usr/bin/env python
# -*-coding:utf-8 -*-
# Author     ：Campanula 梦芸 何
import struct
from typing import List

from matplotlib import pyplot as plt

sec = 5

def read_byte_data(filename) -> List[int]:
    binary_data = open(filename, 'rb').read()
    print(len(binary_data))
    byte_arr = [(struct.unpack("h", binary_data[i:i + 2])[0] if len(binary_data[i:i + 2]) == 2 else 0) for i in
                range(0, len(binary_data), 2)]
    return byte_arr[:100000*sec]


def plot_data(data_arr: List[int], title=""):
    x = range(0, len(data_arr))
    print(len(data_arr))
    y = [d * 64 for d in data_arr]
    plt.figure(figsize=(29.2, 10.8))
    plt.scatter(x, y, s=0.5)
    plt.title(title)
    plt.show()


def draw_data(filename):
    data_arr = read_byte_data(filename)
    plot_data(data_arr, filename)


if __name__ == '__main__':
    fname = ""
    for i in range(0, 4):
        draw_data(fname + str(i))
