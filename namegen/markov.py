#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
from random import choice


class CharChain:
    def __init__(self, order):
        # the order of Markov Chain
        self.order = order
        # initial states
        self.initials = []
        # transportation matrix
        self.trans = {}
        # initials start with certain prefix
        self.prefix = {}

    def update(self, s: str):
        """add a single word to the dictionary"""
        if len(s) < self.order + 1:
            return

        state = s[:self.order]
        self.initials.append(state)

        for l in range(self.order):
            self.prefix.setdefault(state[:l + 1], []).append(state)

        for char in s[self.order:]:
            self.trans.setdefault(state, []).append(char)
            state = state[1:] + char

    def train(self, f):
        """build the dictionary from file"""
        with open(f, 'r', encoding='utf-8') as file:
            for line in file.readlines():
                words = re.findall(r'\w+', line)
                for word in words:
                    self.update(word.lower())
        print('Successfully built. Dict size : %d, %d' % (len(self.initials), len(self.trans)))

    def generate(self, length, initial='') -> str:
        """generate a random sentence which start with given initial"""
        if not self.trans:
            raise ValueError('Cannot generate from an empty dictionary')

        if initial == '' or len(initial) > self.order:
            initial = choice(self.initials)
        else:
            try:
                initial = choice(self.prefix[initial])
            except KeyError:
                initial = choice(self.initials)

        if length <= self.order:
            return initial[:length]

        state = initial
        sentence = [initial, ]
        for i in range(length - self.order):
            try:
                char = choice(self.trans[state])
            except KeyError:
                break
            sentence.append(char)
            state = state[1:] + char

        return ''.join(sentence)


def main():
    chain2 = CharChain(2)
    chain2.train('names.txt')
    print('Chain with order 2:')
    for i in range(10):
        print(chain2.generate(8))

    chain3 = CharChain(3)
    chain3.train('names.txt')
    print('Chain with order 3:')
    for i in range(10):
        print(chain3.generate(8))

    print('Chain with order 3 start with fa:')
    for i in range(10):
        print(chain3.generate(8, 'fa'))


if __name__ == '__main__':
    main()
