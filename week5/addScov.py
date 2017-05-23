'''
Adds the scov fields to the output of blast databases
scov is calculated as lenght/slen * 100
'''

import csv
out1 = []

with open('gnome1.processed.txt') as f:
	reader = csv.reader(f, delimiter='\t')
	next(reader) #skip header
	for line in reader:
		line2 = line + [(float(line[8])/float(line[3]))*100]
		out1.append(line2)
#write to file
csv.writer(open('gnome1.processed.scov.txt', 'w'), delimiter='\t').writerows(out1)

out2 = []
with open('gnome2.processed.txt') as f:
	reader = csv.reader(f, delimiter='\t')
	next(reader) #skip header
	for line in reader:
		line2 = line + [(float(line[8])/float(line[3]))*100]
		out2.append(line2)
#write to file
csv.writer(open('gnome2.processed.scov.txt', 'w'), delimiter='\t').writerows(out2)
