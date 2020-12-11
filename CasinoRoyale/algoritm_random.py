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


def x32(x):
    return x & 0xffffffff


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


class Mt19937:
    def __init__(self, seed=1, n=624, m=397):
        self.n = n
        self.m = m
        self.__upper_mask = 0x80000000
        self.__lower_mask = 0x7fffffff
        self.__seed = seed
        self.states = []
        self.__index = 1
        self._create_states()

    def _create_states(self):
        self.states.append(self.__seed)
        while self.__index < self.n:
            temp = 0x6c078965 * (self.states[self.__index - 1] ^ (self.states[self.__index - 1] >> 30)) + self.__index
            self.states.append(x32(temp))
            self.__index += 1

    def next(self):
        if self.__index >= self.n:
            self._twist()
        x = self.states[self.__index]
        x ^= x >> 11
        x ^= (x << 7) & 0x9d2c5680
        x ^= (x << 15) & 0xefc60000
        x ^= x >> 18
        self.__index += 1
        return x32(x)

    def _twist(self):
        for i in range(self.n):
            temp = x32((self.states[i] & self.__upper_mask) + (self.states[(i + 1) % self.n] & self.__lower_mask))
            self.states[i] = self.states[(i + self.m) % self.n] ^ (temp >> 1)
            if temp & 1 != 0:
                self.states[i] ^= 0x9908b0df
        self.__index = 0


class Mt(Mt19937):
    def _crack(self, mt: Mt19937, user_date):
        user_date = user_date - dt.datetime.fromtimestamp(0, dt.timezone.utc)
        mt.__init__(int(user_date.total_seconds()), self.n, self.m)