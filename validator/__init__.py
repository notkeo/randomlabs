import math
from random import uniform


def sequenator(seq, intervals):
    step = (max(seq) - min(seq)) / intervals
    m = min(seq)
    freq = [0.0] * intervals
    for i in xrange(intervals):
        for x in seq:
            if m < x <= m + step:
                freq[i] += 1
        m += step
    return freq


def approximate(n, p):
    return n + math.sqrt(2 * n) * p + (2 / 3) * p ** 2 - 2 / 3 + 1 / math.sqrt(n)


def sertest(seq, dd=6):
    counter = {}
    for j in xrange(0, len(seq), 2):
        key = int(seq[j] * dd + seq[j + 1] * dd)
        val = counter.get(key)
        if val is None: val = 0
        counter[key] = val + 1
    s = 0.0
    e = float(len(seq)) / (dd ** 2)
    for i in counter.values():
        s += ((i - e) * (i - e)) / e
    print "left", approximate(dd * dd - 1, -1.64)
    print "d", s
    print "right", approximate(dd * dd - 1, 1.64)
    print "Serial test:", approximate(dd ** 2 - 1, -1.64) < s/2 < approximate(dd ** 2 - 1, 1.64)


def ktest(seq):
    seq.sort()
    l = len(seq)
    m = max(seq) - min(seq)
    dm1 = max([x / (l * m) - seq[x - 1] for x in range(1, len(seq) + 1)])
    dm2 = max([seq[x - 1] - (x - 1) / (l * m) for x in range(1, len(seq) + 1)])
    d = max([dm1, dm2])
    y = 1.36 / math.sqrt(l - 1)
    print "KS test:", d < y


def chis_test(seq, intervals=32):
    lower, lager = approximate(intervals - 1, -1.64), approximate(intervals - 1, 1.64)
    e = len(seq) / intervals
    counter = sequenator(seq, intervals)
    s = 0
    for i in xrange(intervals): s += ((counter[i] - e) ** 2) / e
    print "Chis test:", lower < s < lager


seq1 = [uniform(0, 1) for x in xrange(1000)]
chis_test(seq1)
ktest(seq1)
sertest(seq1)
