'''
Changes format of identifier in the TCDB.faa file
Prints formatted identifierand concatenated sequence
for each sequence in file
'''

with open('TCDB.faa', 'r') as f:
	data = list(f)

out = {}
toconcat = []
for line in data:
	if line[0] == '>':
		line = line.split('|')
		ID = line[3].split(' ')[0] + '-' + line[2]
		out[ID] = ''.join(toconcat)
		toconcat = []
	else:
		toconcat.append(line.strip())

for key, value in out.items():
	print key, '\t', value
	
