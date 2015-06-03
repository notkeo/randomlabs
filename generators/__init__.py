# coding: utf8


class Additive:
    @staticmethod
    def help():
        return "[*] add: [[seed array of numbers], modulus]"

    def __init__(self, args, count):
        self.count = count
        self.seed = args[0]
        self.m = args[1]

    def next_value(self):
        for x in range(self.count):
            current_value = (self.seed[0] + self.seed[-1]) % self.m
            self.seed = self.seed[1:]
            self.seed.append(current_value)
            yield current_value


class Linear:
    @staticmethod
    def help():
        return "[*] lc: [seed, multiplier, increment ,modulus] "

    def __init__(self, args, count):
        self.count = count
        self.seed = args[0]
        self.a = args[1]
        self.c = args[2]
        self.m = args[3]

    def next_value(self):
        current_value = self.seed
        for x in range(self.count):
            current_value = (current_value * self.a + self.c) % self.m
            yield current_value


class LFSR:
    @staticmethod
    def help():
        return "[*] lfsr: [seed_number,[array of polynom degs],required bitlen for output numbers]"

    def create_seed(self, tmp_seed):
        tmp_seed = bin(tmp_seed)[2:]
        if len(tmp_seed) < self.max_deg:
            tmp_seed = tmp_seed[:self.max_deg]
        else:
            tmp_seed.zfill(self.max_deg)
        return [int(x) for x in tmp_seed]

    def __init__(self, args, count):
        self.count = count
        self.mask = args[1]
        self.max_deg = max(self.mask)
        self.seed = self.create_seed(args[0])
        self.bitlen = int(args[2])

    def next_value(self):
        for x in range(self.count):
            result = []
            for i in range(self.bitlen):
                random_bit = sum([self.seed[x] for x in self.mask]) % 2
                result.append(random_bit)
                self.seed = self.seed[1:] + [random_bit]
            yield result


class NFSR:
    @staticmethod
    def help():
        return "[*] nfsr: [[seed numbers],[[degs#1],[degs#2],[degs#3]],required bitlen for output numbers]"

    def __init__(self, args, count):
        self.seeds = args[0]
        self.degs = args[1]
        self.bitlen = args[2]
        self.count = count
        self.linear_generators = []
        for x in range(len(self.seeds)):
            self.linear_generators.append(LFSR([self.seeds[x], self.degs[x], 32], self.count))

    def next_value(self):
        for x in range(self.count):
            result = []
            x1 = self.linear_generators[0].next_value().next()
            x2 = self.linear_generators[1].next_value().next()
            x3 = self.linear_generators[2].next_value().next()
            for i in range(self.bitlen):
                result.append((x1[i] * x2[i] ^ x2[i] * x3[i]) ^ x3[i])
            yield result


class Mersenne:
    matrix_a = 0x9908b0df
    highest_mask = (2 ** 32)
    lowest_mask = (2 ** 32) - 1

    @staticmethod
    def help():
        return "[*] mrs: [seed number]"

    def __init__(self, args, count):
        self.count = count
        self.registers = self.create_registers(args[0])
        self.shuffle()

    @staticmethod
    def create_registers(tmp_seed):
        seed = [tmp_seed]
        for x in range(1, 624):
            seed.append(((1812433253 * (seed[x - 1] ^ (seed[x - 1] >> 30))) + x) & 0xFFFFFFFF)
        return seed

    def next_value(self):
        for x in range(self.count):
            if x % 624 is 0:
                self.shuffle()
            y = self.registers[x % 624]
            y ^= (y >> 11)
            y ^= (y << 7 & 0x9d2c5680)
            y ^= (y << 15 & 0xefc60000)
            y ^= (y >> 18)
            yield y

    def shuffle(self):
        for i in range(623):
            y = self.registers[i] & self.highest_mask + (self.registers[i + 1 % 624] & self.lowest_mask)
            self.registers[i] = self.registers[(i + 397) % 624] ^ (y >> 1)
            if y % 2 != 0:
                self.registers[i] ^= self.matrix_a


class RC4:
    @staticmethod
    def help():
        return "[*] rc4: [seeds (any size >0)]"

    def initialize(self, key):
        k = range(0, 256)
        j = 0
        for i in range(256):
            j = (j + k[i] + key[i % len(key)]) % 256
            k[i], k[j] = k[j], k[i]
        return k

    def __init__(self, args, count):
        self.k = self.initialize(args)
        self.n = count

    def next_value(self):
        k = self.k
        i, j = 0, 0
        for x in range(self.n):
            value = 0
            for x in range(0, 8, 2):
                i = (i + 1) % 256
                j = (j + k[i]) % 256
                k[i], k[j] = k[j], k[i]
                value += k[(k[i] + k[j]) % 256] * 10 ^ x
            yield value


class RSA:
    @staticmethod
    def help():
        return "[*] rsa: [p, q, e, 1 < seed (x0) < pq ]"

    def __init__(self, args, count):
        self.p = args[0]
        self.q = args[1]
        self.n = self.p * self.q
        self.seed = args[3]
        self.e = args[2]
        self.count = count

    def next_value(self):
        bit = self.seed
        for x in range(self.count):
            value = []
            for i in range(32):
                bit = int(pow(bit, self.e, self.n))
                value.append(bin(bit)[-1])
            yield int(''.join(value), 2)


class BSS:
    @staticmethod
    def help():
        return "[*] bss: [n, 1 < seed (x) < n ] where n = pq and x = 1 mod n"

    def __init__(self, args, count):
        self.n = args[0]
        self.x = args[1]
        self.count = count

    def next_value(self):
        xq = self.x
        for x in range(self.count):
            mask = 1
            value = 0
            for x in xrange(32):
                xq = (xq ** 2) % self.n
                value |= (xq & mask)
                value <<= x
            yield xq
