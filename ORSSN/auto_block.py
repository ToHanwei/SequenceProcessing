import os
import sys

indir = sys.argv[1]
template = sys.argv[2]
scoredir = sys.argv[3]
identdir = sys.argv[4]

infiles = os.listdir(indir)
runfiles = [os.path.join(indir, infile) for infile in infiles]


with open(template) as tempf:
	lines = tempf.readlines()


for i in range(len(infiles)):
	infile1 = runfiles[i]
	out1 = infiles[i]
	for j in range(i+1, len(infiles)):
		infile2 = runfiles[j]
		out2 = infiles[j]
		script = os.path.join('scripts', out1+'_'+out2+'.lsf')
		logout = os.path.join('logout', out1+'_'+out2+".out")
		logerr = os.path.join('logerr', out1+'_'+out2+".err")
		jobname = infile1 + '_' + infile2
		outlines = []
		command = (
			"python CalulateProSimMatrix_block2block.py"
			+ " -i1 " + infile1
			+ " -i2 " + infile2
			+ " -m " + "./blosum/blosum80.bla"
			+ " -s " + scoredir
            + " -d " + identdir
			)

		outlines.append(lines[0])
		outlines.append(lines[1].strip() + ' ' + jobname + '\n')
		outlines.append(lines[2].strip() + ' ' + logerr + '\n')
		outlines.append(lines[3].strip() + ' ' + logout + '\n')
		outlines.append(lines[4].strip() + ' zhaolab\n')
		outlines.append(lines[5])
		outlines.append('\n')
		outlines.append(command + '\n')
		with open(script, 'w') as tempf:
			tempf.writelines(outlines)
		
		os.system('bsub < ' + script)
		os.remove(script)
