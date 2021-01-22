#/usr/bin/python
#codeing:utf-8

import os
import argparse
from functools import reduce
import pandas as pd
import numpy as np
from pandas import DataFrame
from collections import defaultdict


def ArgParse():
	parser = argparse.ArgumentParser(description="Calculate simility of sequence aligment")
	parser.add_argument('-i1', '--inputfile1', action='store', 
						help='input the sequence aligment file')
	parser.add_argument('-i2', '--inputfile2', action='store', 
						help='input the sequence aligment file')
	parser.add_argument('-m', '--matrix', action='store', default='BLUSUM62.csv',
						help='input the matrix file and must be csv file format')
	parser.add_argument('-s', '--scoredir', action='store', 
						help='similarity score outdir')
	parser.add_argument('-d', '--identdir', action='store', 
						help='identity outdir')
	args = parser.parse_args()
	return args

def MsaSequence(infile):
	with open(infile) as MsaFile:
		MsaSeq = MsaFile.read()
	SeqList = MsaSeq.split(">")[1:]
	SeqProce = []
	for seq in SeqList:
		SeqLine = seq.split("\n")
		SeqName = SeqLine[0]
		SeqValue = ''.join(SeqLine[1:])
		SeqProce.append((SeqName, SeqValue))
	return SeqProce


def clear_gap(seqi, seqj):
	seqpare = zip(seqi, seqj)
	seqpare = [ele for ele in seqpare if ele != ('-', '-')]
	seqi, seqj = list(zip(*seqpare))
	return seqi, seqj

	
def ClaulateSimi(Seqs1, Seqs2, file_matrix):
	BLOSUM = pd.read_csv(file_matrix, index_col=0)
	Data = {}
	Leng, Index = len(BLOSUM), BLOSUM.index
	for i in range(Leng):
		for j in range(Leng):
			Data[Index[i]+Index[j]] = BLOSUM.iloc[i][j]
	ResList = []
	IdeList = []
	for i_name, i_seq in Seqs1:
		for j_name, j_seq in Seqs2:
			Score = 0
			ident = 0
			ii_seq, jj_seq = clear_gap(i_seq, j_seq)
			seqlen = len(ii_seq)
			for k in range(seqlen):
				i_aad = ii_seq[k]
				j_aad = jj_seq[k]
				try:
					S = Data[i_aad+j_aad]
				except KeyError:
					S = 0
				siden = 1 if (i_aad == j_aad) else 0
				Score += S
				ident += siden
			Score = Score / seqlen
			ident = 100 * ident / seqlen
			Score = round(Score, 3)
			ident = round(ident, 3)
			ResList.append(i_name+"\t"+j_name+"\t"+str(Score)+"\n")
			IdeList.append(i_name+"\t"+j_name+"\t"+str(ident)+"\n")
	return ResList, IdeList

def main():
	args = ArgParse()
	file_matrix = args.matrix
	file_input1 = args.inputfile1
	file_input2 = args.inputfile2
	scoredir = args.scoredir
	identdir = args.identdir
	
	prefix1 = os.path.split(file_input1)[1]
	prefix2 = os.path.split(file_input2)[1]
	prefix = prefix1 + "_" + prefix2
	scoreout = os.path.join(scoredir, prefix+'.score')
	identout = os.path.join(identdir, prefix+'.ident')

	Seqs1 = MsaSequence(file_input1)
	Seqs2 = MsaSequence(file_input2)
	ResList, IdeList = ClaulateSimi(Seqs1, Seqs2, file_matrix)

	with open(scoreout, 'w') as out:
		out.writelines(ResList)
	with open(identout, 'w') as out:
		out.writelines(IdeList)

if __name__ == "__main__":
	main()
