from functools import reduce
from math import gcd

def egcd(a, b):
    if a == 0:
        return b, 0, 1
    else:
        g, x, y = egcd(b % a, a)
        return g, y - (b // a) * x, x


def mod_inv(b, n):
    g, x, _ = egcd(b, n)
    if g == 1:
        return x % n


class Lcg:
    # a its "multiplier", c its "increment", m its "modulus"
    def __init__(self, seed=0, a=None, c=None, m=None):
        self.state = seed
        self.a = a
        self.c = c
        self.m = m

    def next(self):
        fg = True
        if self.a is None:
            print('unknown a')
            fg = False
        if self.a is None:
            print('unknown b')
            fg = False
        if self.a is None:
            print('unknown c')
            fg = False
        if fg:
            self.state = (self.state * self.a + self.c) % self.m
        return self.state

    def _crack_unknown_increment(self, states):
        if self.m is None or self.a is None:
            return "Error a or/and m unknown"
        self.c = (states[1] - states[0] * self.a) % self.m
        return "Found с"

    def _crack_unknown_multiplier(self, states):
        if self.m is None:
            return "Error m unknown"
        mi = mod_inv(states[1] - states[0], self.m)
        self.a = (states[2] - states[1]) * mi % self.m
        self._crack_unknown_increment(states)
        return "Found a, c"

    def _crack_unknown_modulus(self, states):
        diffs = [s1 - s0 for s0, s1 in zip(states, states[1:])]
        zeroes = [t2 * t0 - t1 * t1 for t0, t1, t2 in zip(diffs, diffs[1:], diffs[2:])]
        self.m = abs(reduce(gcd, zeroes))
        self._crack_unknown_multiplier(states)
        return "Found a, c, m"

    def _crack(self, states, count_of_parameters):
        if count_of_parameters == 3:
            return self._crack_unknown_modulus(states)
        elif count_of_parameters == 2:
            return self._crack_unknown_multiplier(states)
        else:
            return self._crack_unknown_increment(states)