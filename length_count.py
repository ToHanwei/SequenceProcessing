import sys
import matplotlib.pyplot as plt

filename = sys.argv[1]
namesfile = sys.argv[2]
#low = int(sys.argv[2])
#high = int(sys.argv[3])
#outfile = sys.argv[4]

with open(namesfile) as namef:
	names = [line.strip() for line in namef]

with open(filename) as seqfile:
	seqs = seqfile.read().split(">")

count_dict = {}

for seq in seqs:
	lines = seq.split("\n")
	name = lines[0]
	aads = "".join(lines[1:])
	length = str(len(aads))
	#if length < low: continue
	#if length > high: continue
	count_dict[name] = length


outfile = filename + "_length"
with open(outfile, 'w') as out:
	out.write("names\tlength\n")
	for key in names:
		if key in count_dict.keys():
			line = key + "\t" + count_dict[key]+"\n"
		else:
			line = key + "\tNone\n"
		out.write(line)

