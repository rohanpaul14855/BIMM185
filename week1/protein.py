'''
Finds protein associations for the first 2000 proteins
in RS.txt.bz2 file. Then outputs most likely associated proteins
based on P-value. 
'''

import bz2

prots = {}
f = bz2.BZ2File('RS.txt.bz2', 'r')
while len(prots) <= 2000:
	line = next(f).split('\t')
	if line[0] not in prots.keys():
		prots[line[0]] = [[line[1], float(line[3].strip())]]
	else:
		prots[line[0]].append([line[1], float(line[3].strip())])
for line in f:
	if line[0] in prots.keys():
		prots[line[0]].append([line[1], float(line[3].strip())])	

good_pairs = []
for key, value in prots.items():
	v = sorted(value, key = lambda x: x[1])
	good_pairs.append([key, v[-1][0], v[-1][1], len(v)])

for t in sorted(good_pairs, key=lambda x: x[-1]):
	print t

