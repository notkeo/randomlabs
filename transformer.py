from argparse import ArgumentParser
import argparse
import sys

from transformers import Transformer


def createArgsParser():
    parser = ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("-f", help="input file name")
    parser.add_argument("-d", help="distribution name")
    parser.add_argument("-p", help="params vector")
    return parser


def main():
    parser = createArgsParser()
    args = parser.parse_args(sys.argv[1:])
    input = []
    try:
        for x in open(args.f):
            input += [float(x)]
    except:
        print "can't open file - " + args.f

    trans = Transformer(input)
    args.p = eval(args.p)

    if args.d == 'st': out = trans.toUniform(args.p[0], args.p[1]),
    if args.d == 'tr': out = trans.toTriangular(args.p[0], args.p[1]),
    if args.d == 'ex': out = trans.toExpo(args.p[0], args.p[1]),
    if args.d == 'nr': out = trans.toNormal(args.p[0], args.p[1]),
    if args.d == 'gm': out = trans.toGamma(args.p[0], args.p[1], args.p[2]),
    if args.d == 'ln': out = trans.toLgNormal(args.p[0], args.p[1]),
    if args.d == 'ls': out = trans.toLgStat(args.p[0], args.p[1]),
    if args.d == 'bi': out = trans.toBinom(args.p[0], args.p[1])

    f = open("./out/" + args.d + '_transformed_seq.txt', 'w')
    for x in out[0]:
        f.write(str(x))
        f.write("\n")
    f.close()


if __name__ == '__main__':
    main()