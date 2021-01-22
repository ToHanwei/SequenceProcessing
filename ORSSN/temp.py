import os
from multiprocessing import Process

files = os.listdir('block2block_out')


def func(_file):
    infile = os.path.join('block2block_out', _file)
    oufile = os.path.join('block2block_out_more2', _file)
    fout = open(oufile, 'w')
    outlist = []
    for line in open(infile):
        ls = line.strip().split()
        if float(ls[2]) > 2:
            outlist.append(line)
    fout.writelines(outlist)
    fout.close()

jobs = []

for _file in files:
    p = Process(target=func, args=(_file,))
    p.start()
    jobs.append(p)

for i in range(0, len(jobs), 70):
    for j in range(i, i+70):
        p = jobs[j]
        p.join()
