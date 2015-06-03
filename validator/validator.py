__author__ = 'notkeo'

import math

from  transformer import Transformer


def chi2(act, exp):
    v = 0
    for a, e in zip(act, exp):
        if e > 0:
            v += (a - e) ** 2 / e
    return v


cache_stirl = {}


def Stirling(n, k):
    def stirlf(n, k):
        if k == n: return 1L
        if k == 1: return 1L
        return long(Stirling(n - 1, k - 1) + k * Stirling(n - 1, k))

    if cache_stirl.has_key((n, k)): return cache_stirl[(n, k)]
    return cache_stirl.setdefault((n, k), stirlf(n, k))


def chi(sequence, d=16):
    range = (7.261, 25.00)
    actual = [0] * d
    expected = [(len(sequence) / float(d))] * d
    for x in sequence:
        actual[int(x * d)] += 1
    v = chi2(actual, expected)
    print "test name:", "chi-squared"
    print "vertex of freedom:", d
    print "range: ", range
    print "statistic value: ", v
    print "result:", range[0] <= chi2(actual, expected) <= range[1]
    print("-----------------------")


def serial(sequence, d=8):
    range = (45.74, 82.53)
    actual = (d * d) * [0]
    expected = (d ** 2) * [len(sequence) / (2 * float(d) ** 2)]
    for i in xrange(len(sequence) / 2):
        q, r = sequence[2 * i], sequence[2 * i + 1]
        actual[int((float(q) * d * d + float(r) * d) % (d * d))] += 1
    v = chi2(actual, expected)
    print "test name:", "serial test"
    print "vertex of freedom:", d * d
    print "range: ", range
    print "statistic value: ", v
    print "result:", range[0] <= chi2(actual, expected) <= range[1]
    print("-----------------------")


def gap(sequence, d=16):
    range = (2.167, 14.07)
    gaps = len(sequence) / 10
    j, s, actual = -1, 0, 8 * [0]
    while s != gaps and j != len(sequence):
        j, r = j + 1, 0
        while j != len(sequence) and int(sequence[j] * d) < d / 2:
            j, r = j + 1, r + 1
        actual[min(r, 7)] += 1
        s += 1
    pd = 0.5
    expected = [(gaps * pd * (1.0 - pd) ** r) for r in xrange(7)]
    expected += [gaps * (1.0 - pd) ** 7]
    v = chi2(actual, expected)
    print "test name:", "gaps test"
    print "vertex of freedom:", 8
    print "range: ", range
    print "statistic value: ", v
    print "result:", range[0] <= chi2(actual, expected) <= range[1]
    print("-----------------------")


def poker(sequence, d=16):
    sequence = [int(x * d) for x in sequence]
    range = (0.7107, 9.488)
    actual = 5 * [0]
    for l in xrange(len(sequence) / 5):
        hand = sequence[l * 5:l * 5 + 5]
        vUnique = [v in hand for v in xrange(d)]
        distinct = reduce(lambda a, b: a + b, vUnique, 0)
        actual[distinct - 1] += 1

    def expectedFreq(n, d):
        k = 5
        exp = 5 * [0]
        for r in xrange(1, 6):
            p = 1.0
            for i in xrange(r):
                p *= d - i
            exp[r - 1] = (n / 5) * (p / float(d) ** k) * Stirling(k, r)
        return exp

    expected = expectedFreq(len(sequence), d)
    v = chi2(actual, expected)
    print "test name:", "poker test"
    print "vertex of freedom:", d
    print "range: ", range
    print "statistic value: ", v
    print "result:", range[0] <= chi2(actual, expected) <= range[1]
    print("-----------------------")


def permutation(sequence, t=4):
    range = (13.09, 35.17)
    t, fc = 4, math.factorial(4)
    actual = fc * [0]
    for i in xrange(len(sequence) / t):
        u = sequence[t * i:t * i + t]
        c = t * [0]
        r = t
        while r > 0:
            s = 0
            for j in xrange(r):
                if u[j] > u[s]: s = j
            c[r - 1] = s
            u[r - 1], u[s] = u[s], u[r - 1]
            r -= 1
        f = 0
        for j in xrange(t - 1):
            f = (f + c[j]) * (j + 2)
        f += c[t - 1]
        actual[f] += 1
    expected = fc * [len(sequence) / float(t) / fc]
    v = chi2(actual, expected)
    print "test name:", "permutations test"
    print "vertex of freedom:", fc
    print "range: ", range
    print "statistic value: ", v
    print "result:", range[0] <= chi2(actual, expected) <= range[1]
    print("-----------------------")


def monotonic(sequence, d=1024):
    range = (1.145, 11.070)
    last, thisSeqLen = sequence[0], 1
    actual = 7 * [0]
    for i in sequence[1:]:
        if i > last:
            last, thisSeqLen = i, thisSeqLen + 1
        else:
            actual[min(thisSeqLen, 6)] += 1
            last, thisSeqLen = i, 1
    actual[min(thisSeqLen, 6)] += 1

    def expectedChi2(actual, n):
        a = [[4529.4, 9044.9, 13568.0, 18091.0, 22615.0, 27892.0],
             [9044.9, 18097.0, 27139.0, 36187.0, 45234.0, 55789.0],
             [13568.0, 27139.0, 40721.0, 54281.0, 67852.0, 83685.0],
             [18091.0, 36187.0, 54281.0, 72414.0, 90470.0, 111580.0],
             [22615.0, 45234.0, 67852.0, 90470.0, 113262.0, 139476.0],
             [27892.0, 55789.0, 83685.0, 111580.0, 139476.0, 172860.0]]
        b = [1.0 / 6.0, 5.0 / 24.0, 11.0 / 120.0, 19.0 / 720.0, 29.0 / 5040.0, 1.0 / 840.0]
        V = 0.0
        for i in xrange(6):
            for j in xrange(6):
                V += (actual[i + 1] - n * b[i]) * (actual[j + 1] - n * b[j]) * a[i][j]
        return V / n

    v = expectedChi2(actual, len(sequence))
    print "test name:", "monotonic test"
    print "vertex of freedom: 6"
    print "range: ", range
    print "statistic value: ", v
    print "result:", range[0] <= v <= range[1]
    print("-----------------------")


def conflict(sequence, d=2, k=13):
    range = (0.05, 0.95)
    sequence = [int(x * d) for x in sequence]
    actual = {}
    conflicts = 0
    for x in xrange(0, len(sequence), k):
        key = ''.join(str(y) for y in sequence[x:x + k])
        if actual.get(key) is None:
            actual[key] = 0
        if actual[key] == 1:
            conflicts += 1
        actual[key] = 1
    p = getProbability(len(sequence) / k, 1 << k, conflicts)
    print "test name:", "conflict test"
    print "conflicts count: ", conflicts
    print "vertex of freedom: ", d ** k
    print "probability range: ", range
    print "actual probability: ", p
    print "result:", range[0] <= p <= range[1]
    print("-----------------------")


def getProbability(n, m, x):
    a = (n + 1) * [0]
    bound = 1e-20
    a[1] = 1
    j0, j1 = 1, 1
    for i in xrange(n - 1):
        j1 += 1
        for j in xrange(j1, j0 - 1, -1):
            b = (float(j) / float(m))
            a[j] = b * a[j] + ((1 + 1.0 / m) - b) * a[j - 1]
            if a[j] < bound:
                a[j] = 0
                if j == j1:
                    j1 -= 1
                else:
                    if j == j0:
                        j0 += 1
    p = 0.0
    current = 0
    i = n
    while current < x:
        i -= 1
        current += 1
        p += a[i]
    if math.fabs(p - 1) < 1e-10:
        p = 1
    return p


sx = [int(x) for x in open("sequence.txt")]
if (max(sx) > 1):
    t = Transformer(sx)
    s = t.toUniform(0, 1)
chi(s)
serial(s)
gap(s)
poker(s)
permutation(s)
monotonic(s)
conflict(s)

nb = input()