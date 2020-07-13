#!coding:utf-8

import sys
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
from collections import Counter


infile1 = sys.argv[1]
infile2 = sys.argv[2]
# outfile = sys.argv[3]

aads = ['A', 'C', 'D', 'E', 'F', \
		'G', 'H', 'I', 'K', 'L', \
		'M', 'N', 'P', 'Q', 'R', \
		'S', 'T', 'V', 'W', 'Y', \
		'X', '-']


def procefile(infile):
	with open(infile) as seqf:
		seqs = seqf.read().split('>')[1:]
	num_of_seq = len(seqs)
	seques = []
	for seq in seqs:
		lines = seq.strip().split('\n')
		name = lines[0]
		seq = ''.join(lines[1:])
		seques.append(seq)
	return num_of_seq, seques


def conarray(seqtuple):
	countd = []
	nums, seques = seqtuple
	sites = list(zip(*seques))
	for site in sites:
		sitedict = {aad: 0 for aad in aads}
		c = Counter(site)
		outc = [c[i]/nums for i in aads]
		countd.append(outc)
	#countd = np.array(countd)
	return countd


def JS_divergence(stat):
	p = np.array(stat[0])
	q = np.array(stat[1])
	M = (p + q) / 2
	KL_pM = stats.entropy(p, M)
	KL_qM = stats.entropy(q, M)
	js = 0.5*KL_pM + 0.5*KL_qM
	return js


def main():
	seqtuple1 = procefile(infile1)
	seqtuple2 = procefile(infile2)
	array1 = conarray(seqtuple1)
	array2 = conarray(seqtuple2)
	stats = zip(array1, array2)
	res = map(JS_divergence, stats)
	res = list(res)
	#plt.plot(range(1, len(res)+1), res)
	#plt.show()
	for i, r in enumerate(res):
		print(i+1, r)


if __name__ == "__main__":
	main()


