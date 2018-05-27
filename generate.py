#!/usr/bin/python
# -*- coding: utf-8 -*-

import pickle

from namegen import markov

NAMELIST = 'names.txt'


def main():
    order = input('Input the order of Markov chain (1 <= order <= 5, default is 2):')
    try:
        order = int(order)
        if not 1 <= order <= 5:
            raise ValueError
    except ValueError:
        order = 2

    length = input('Input the max length of each name (default is 6):')
    try:
        length = int(length)
    except ValueError:
        length = 6

    initial = input('Input the letter(s) that the name start with (length not exceed the order, default is random):')

    num = input('Input the number of names to generate (1 <= n <= 100, default is 10):')
    try:
        num = int(num)
        if not 1 <= num <= 100:
            raise ValueError
    except ValueError:
        num = 10

    filename = 'chain_%d' % order
    try:
        with open(filename, 'rb') as f:
            chain = pickle.load(f)
        print('Read from file successfully.')
    except FileNotFoundError:
        chain = markov.CharChain(order)
        chain.train(NAMELIST)
        with open(filename, 'wb') as f:
            pickle.dump(chain, f)

    for i in range(num):
        print(chain.generate(length, initial))


if __name__ == '__main__':
    main()
