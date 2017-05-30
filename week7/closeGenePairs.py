'''
Finds gene pairs that are conserved across the two genomes
Return gene pairs that are within 5 genes of each other
output format:
Gene 1 in E. coli
Gene 2 in E. coli
Distance in E. coli (in genes)
Distance of their orthologs in A. tumefaciens (in genes).
'''


import MySQLdb
import csv

sqldb = MySQLdb.connect(host="bm185s-mysql.ucsd.edu", user="bm185sag", passwd="Arturo!*", db="bm185sag_db")
cur = sqldb.cursor()
cur.execute('SELECT * FROM homology_1;')
pairs = [list(k) for k in cur.fetchall()]
cur2 = sqldb.cursor()
cur2.execute('SELECT g.gene_id, g.replicon_id FROM genes2 g;')
replicons = {k[0]: k[1] for k in cur2.fetchall()}

out = []
prev_pair = pairs[0]
for i, pair in enumerate(pairs):
	if i == 0:
		continue
	left = abs(prev_pair[0] - pair[0]) <= 5
	right = abs(prev_pair[1] - pair[1]) <= 5
	replicon_check = replicons[prev_pair[1]] == replicons[pair[1]]
	if left and right and replicon_check:
		out.append([prev_pair[0], pair[0], pair[0] - prev_pair[0], pair[1] - prev_pair[1]])	
	prev_pair = pair
		
with open('closeGenes.txt' , 'w') as f:
	csv.writer(f, delimiter='\t').writerows(out)



