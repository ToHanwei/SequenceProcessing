#!coding:utf-8

import itertools
import argparse
import tmhmm

"""
Batch statistic TM number in sequences
Input, FASTA format file.
Output, a summary file.
"""


def Commandline():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', dest='sequence_file',
                        type=argparse.FileType('r'), required=True,
                        help='path to file in fasta format with sequences')
    parser.add_argument('-m', '--model', dest='model_file',
                        default="TMHMM2.0.model",
                        help='path to the model to use')
    parser.add_argument('-c', '--cutoff', dest='cutoff',
                        default=18, type=int,
                        help='Tm cutoff value.')
    parser.add_argument('-o', '--outfile', dest='out_file',
                        help='output file path')
    args = parser.parse_args()
    return args


def summarize(path):
    """
    Summarize a path as a list of (start, end, state) triples.
    """
    for state, group in itertools.groupby(enumerate(path), key=lambda x: x[1]):
        group = list(group)
        start = min(group, key=lambda x: x[0])[0]
        end = max(group, key=lambda x: x[0])[0]
        yield start, end, state

def parsefasta(seqfile):
    """
    Parser a FASTA format file as sequence and header
    """
    seqs = seqfile.read().split('>')[1:]
    for seq in seqs:
        lines = seq.split('\n')
        header = lines[0]
        sequence = ''.join(lines[1:])
        yield header, sequence


def main():
    args = Commandline()
    seqfile = args.sequence_file
    model = args.model_file
    cutoff = args.cutoff
    outfile = args.out_file
    outf = open(outfile, 'w')
    # parser FASTA format file
    for header, sequence in parsefasta(seqfile):
        count = 0
        try:
            annotation = tmhmm.predict(sequence, header, model, compute_posterior=False)
        except KeyError:
            #sequence = sequence.replace('X', 'F')
            #sequence = sequence.replace('Z', 'F')
            continue
        for start, end, state in summarize(annotation):
            if (state == 'M') and (abs(end-start)>=cutoff):
                count += 1
        print(header+'\t'+str(count), file=outf)

if __name__ == "__main__":
    main()
