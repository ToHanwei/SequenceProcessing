#!coding:utf-8

"""
Detail:
Split a large FASTA format file into a small file,
that specifies the number sequences
Variate:
Num_SEQ_PER_FILE
---the number of specified sequences contained in the small file
LARGE_FILE
---the large sequences FASTA format file name
SEQ_DIR
---Store split files
"""

__author__ = "wei"
__date__ = "20190709"
__email__ = "hanwei@shanghaitech.edu.cn"

import sys
import os

Num_SEQ_PER_FILE = 1600
LARGE_FILE = sys.argv[1]
SEQ_DIR = sys.argv[2]

count=1
with open(LARGE_FILE) as SeqFile:
	num_seq = -1
	write_list = []
	for line in SeqFile:
		if line[0] == ">":
			num_seq += 1
		write_list.append(line)
		if num_seq == Num_SEQ_PER_FILE:
			SplitFile = os.path.join(SEQ_DIR, "Split"+str(count))
			with open(SplitFile, 'w') as OutFile:
				OutFile.writelines(write_list[:-1])
				write_list = [write_list[-1]]
				num_seq = 0
				count += 1
	SplitFile = os.path.join(SEQ_DIR, "Split"+str(count))
	with open(SplitFile, 'w') as OutFile:
		OutFile.writelines(write_list)
