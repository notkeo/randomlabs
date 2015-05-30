# coding: utf8
from argparse import ArgumentParser
import argparse
import sys

from generators import *

GENERATORS = {'lc': Linear, 'add': Additive, 'lfsr': LFSR, 'nfsr': NFSR, 'mt': Mersenne, 'rc4': RC4, 'rsa': RSA,
              'bss': BSS}


def merge_help():
    return '\n'.join([g.help() for g in GENERATORS.values()])


def createArgsParser():
    parser = ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-g', metavar='generator', choices=dict(GENERATORS).keys(),
                        help=u"тип используемого генератора. \nДопустимые значения:  " + ",".join(
                            GENERATORS.keys()))
    parser.add_argument('-i', metavar='init',
                        help=u"вектор инициализации. \n Справка: -i help")
    parser.add_argument('-n', metavar='numbers', type=int, default=10000,
                        help=u"количество генерируемых чисел (default: 10000)")
    parser.add_argument('-f', metavar='filename', help=u"имя выходного файла")
    return parser


def generate(args):
    init = eval(args.i)
    generator = GENERATORS[args.g](init, args.n)
    with open(args.f, 'w') as f:
        for x in generator.next_value():
            if args.g == 'lfsr' or args.g == 'nfsr':
                x = int(''.join([str(i) for i in x]), 2)
            f.write(str(x % 1000) + '\n')

def main():
    parser = createArgsParser()
    args = parser.parse_args(sys.argv[1:])
    if args.i == "help":
        print merge_help()
    else:
        if args.f and args.g and args.i:
            generate(args)
        else:
            print "invalid args size"
            parser.print_usage()


if __name__ == '__main__':
    main()