import os
import sys

indir = sys.argv[1]
template = sys.argv[2]
scoredir = sys.argv[3]
identdir = sys.argv[4]

infiles = os.listdir(indir)
scripts = [os.path.join('scripts', infile+'.lsf') for infile in infiles]
runfiles = [os.path.join(indir, infile) for infile in infiles]


with open(template) as tempf:
	lines = tempf.readlines()

for i in range(len(infiles)):
	infile = runfiles[i]
	script = scripts[i]
	logout = os.path.join('logout', infiles[i]+".out")
	logerr = os.path.join('logerr', infiles[i]+".err")
	jobname = infile
	outlines = []	
	command = (
		"python CalulateProSimMatrix_all_to_all_Dict.py"
		+ " -i " + infile
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
