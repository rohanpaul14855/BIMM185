import csv
import numpy as np
import MySQLdb
from scipy import stats
'''
Find intergenic distances for positive and negative training examples
Use a kernel density estimator to train a bayes model
Compute posterior probability for each gene pair
Assign a class to each of these examples based on the probability
'''

sqldb = MySQLdb.connect(host="bm185s-mysql.ucsd.edu", user="bm185sag", passwd="Arturo!*", db="bm185sag_db")
cur = sqldb.cursor()
with open('strongOrConfirmedOperons.ltags.txt', 'r') as f:
	#get genes belonging to operons with strong evidence
	reader = [k[1] for k in csv.reader(f, delimiter='\t')]

#get postive control
cur.execute("SELECT g.gene_id,e.start_pos,e.end_pos,g.strand FROM genes2 g JOIN exons e USING(gene_id) WHERE g.locus_tag IN ({}) ORDER BY e.start_pos ASC;".format("'" + "','".join(reader) + "'"))
pos_table = [list(k) for k in cur.fetchall()]

nr = int(cur.rowcount)
pos = []
row1 = pos_table[0]
#calculate intergenic distances for positive control
for i, row in enumerate(pos_table):
	if i == 0:
		continue
	if row[-1] == row1[-1]:
		if row[-1] == 'F':
			pos.append(abs(int(row[1] - row1[2] + 1)))
		else:
			pos.append(abs(int(row[2] - row1[1] + 1)))
	row1 = row

negcur = sqldb.cursor()
#get negative control
negcur.execute('SET @a:=0')
negcur.execute("SELECT @a := @a + 1 as idx, g.gene_id,e.start_pos,e.end_pos,g.strand FROM genes2 g JOIN exons e USING(gene_id) WHERE g.genome_id = 1 ORDER BY e.start_pos ASC;")

#add a column showing whether the gene belongs to an operon
neg_table = [list(k) for k in negcur.fetchall()]
for row in neg_table:
	if row[1] in [k[0] for k in pos_table]: #check if gene is in an operon
		row.append('operon')
	else:
		row.append('null')
row1 = neg_table[0]
#calculate intergenic distances for negative control
neg = []
for row in neg_table:
	if row[-1] != row1[-1]:	#check whether in the same operon
		if row[-2] == row1[-2]:	#force same strand
			neg.append(abs(int(row[2] - row1[3] + 1)))
	row1 = row

#estimate kernel densitites		
pos_kernel = stats.gaussian_kde(pos, bw_method=0.5)	
neg_kernel = stats.gaussian_kde(neg, bw_method=0.5)
pos_kernel._compute_covariance()
neg_kernel._compute_covariance()
#pplot = [[i, j] for i, j in zip(pos, pos_kernel.pdf(pos))]

pred_table = np.array(neg_table)[:,:5]
prev_row = pred_table[0]
out= []

#assign posterior probabilities
for i, row in enumerate(pred_table):
	if i == 0:
		continue
	posterior = [0]
	if row[-1] == prev_row[-1]:	#check if same strand
		dist = abs(int(row[2]) - int(prev_row[3]) + 1)
		ppos = pos_kernel.evaluate(dist)
		pneg = neg_kernel.evaluate(dist)
		posterior = (ppos * 0.6)/((ppos * 0.6) + (pneg *  0.4))
	hit = 'TP' if posterior >= 0.5 else 'TN'
	out.append([prev_row[1], row[1], dist, hit, posterior[0]])
	prev_row = row
#write to file
with open('tus.txt', 'w') as f:
	csv.writer(f, delimiter='\t').writerows(out)
	




	
