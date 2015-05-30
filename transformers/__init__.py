import math


class Transformer:
    def __init__(self, data):
        self.max = max(data) - min(data)
        if self.max < 1:
            self.data = data
        else:
            self.data = [x / (self.max+1) for x in data]

    def toUniform(self, a, b):
        return [a + (b - a) * v for v in self.data]

    def toTriangular(self, a, b):
        d = self.data
        return [a + b * (d[i] + d[i + 1] - 1) for i in xrange(0, len(d) - 1, 2)]


    def toExpo(self, a, b):
        return [(-b * math.log10(x) + a) for x in self.data if x != 0]


    def toNormal(self, u, q):
        result = []
        for i in xrange(0, len(self.data) - 1, 2):
            result += [u + q * math.sqrt(math.fabs(-2 * math.log10(1 - self.data[i]))) * math.cos(
                2 * math.pi * self.data[i + 1])]
            result += [u + q * math.sqrt(math.fabs(-2 * math.log10(1 - self.data[i]))) * math.sin(
                2 * math.pi * self.data[i + 1])]
        return result

    def toLgNormal(self, a, b):
        d = self.toNormal(0, 1)
        return [a + math.exp(b - x) for x in d]

    def toLgStat(self, a, b):
        d = self.toUniform(0, 1)
        return [a + b * math.log10(x / (1 - x)) for x in d if x != 1]

    def toGamma(self, a, b, c):
        result = []
        d = self.data
        if c > 1.0:
            if int(c) == c:
                for x in xrange(c, len(d)):
                    inverted = (1 - i for i in d[x - c:x])
                    mul = 1
                    for i in inverted:
                        mul *= i
                    result += [a - b * math.log(mul)]
            else:
                ainv = math.sqrt(2.0 * c - 1.0)
                q = c - math.log(4)
                r = c + ainv
                for i in xrange(1, len(d)):
                    u1 = d[i]
                    u2 = d[-i - 1]
                    if not 1e-7 < u1 < .9999999:
                        continue
                    v = math.log(u1 / (1.0 - u1)) / ainv
                    x = c * math.exp(v)
                    z = u1 * u1 * u2
                    r = q + r * v - x
                    if r + 1.0 + math.log(4.5) - 4.5 * z >= 0.0 or r >= math.log(z):
                        result += [a + x * b]

        elif c == 1.0:
            e_data = self.toExpo(0, 1)
            for x in e_data:
                result += a + math.log(x) * b
        else:
            for i in xrange(0, len(d), 2):
                u = d[i]
                b = (math.e + c) / math.e
                p = b * u
                if p <= 1.0:
                    x = p ** (1.0 / c)
                else:
                    x = -math.log((b - p) / c)
                u1 = d[i + 1]
                if p > 1.0:
                    if u1 <= x ** (c - 1.0):
                        result += [a + x * b]
                elif u1 <= math.exp(-x):
                    result += [a + x * b]

        return result

    def toBinom(self, p, n):
        result, k = [], 0
        while len(self.data[n * k:n * k + n]) > 0:
            result += [sum([1 if x <= p else 0 for x in self.data[n * k:n * k + n]])]
            k += 1
        return [result]
