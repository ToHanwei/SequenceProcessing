#!coding:utf-8

import sys

ClusterFileName = sys.argv[1]
with open(ClusterFileName) as ClusterFile:
	ClusterList = ClusterFile.read().split(">Cluster ")
SameList = []
for cluster in ClusterList:
	clusters = cluster.split("\n")
	while '' in clusters:
		clusters.remove('')
	if len(clusters) > 2:
		temp = []
		for access in clusters[1:]:
			access = access.split(", ")[1].split("...")[0][1:]
			temp.append(access)
		SameList.append(temp)

for line in SameList:
	assert len(line) == 2
	if "." in line[0]:
		print(line[0] + "\t" + line[1])
	elif "." in line[1]:
		print(line[1] + "\t" + line[0])
	else:
		print("Something Error!")

