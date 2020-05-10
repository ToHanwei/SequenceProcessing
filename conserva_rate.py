#!coding:utf-8

import os
import sys
import argparse


if len(sys.argv) == 1:
    os.system('python conserva_rate.py --help')
    sys.exit(1)

parser = argparse.ArgumentParser(description='conserva_rate')
parser.add_argument('-f', '--MSAfile', help='MSA output file path, as input file')

