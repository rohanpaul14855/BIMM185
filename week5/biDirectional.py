'''
Queries two blast databases to identify orthologous genes
Uses the bidirectional best hit criteria to identify these gene pairs
'''
import MySQLdb

sqldb = MySQLdb.connect(host="bm185s-mysql.ucsd.edu", user="bm185sag", passwd="Arturo!*", db="bm185sag_db")
cur = sqldb.cursor()
cur.execute('SELECT DISTINCT(qseqid) FROM blast_1 WHERE qcovs >= 60 OR scov >=60;')


prots = []
nr = int(cur.rowcount)
for i in range(nr):
	row = cur.fetchone()
	cur2 = sqldb.cursor()
	cur2.execute("SELECT qseqid, sseqid, bitscore FROM blast_1 WHERE qseqid='{}' ORDER BY bitscore DESC LIMIT 1;".format(row[0]))
	cur3 = sqldb.cursor()
	cur3.execute("SELECT qseqid, sseqid, bitscore FROM blast_2 WHERE sseqid='{}' ORDER BY bitscore DESC LIMIT 1;".format(row[0]))
	q2 = cur2.fetchone()
	q3 = cur3.fetchone()
	if q2[0] == q3[1]:
		#bidirectional hit
		prots.append(q2[1])
cur4 = sqldb.cursor()
cur4.execute('SELECT protein_id,gene_id FROM genes2 WHERE protein_id  IN ({});'.format("'" + "','".join(prots) + "'"))
results = cur4.fetchall()

print(results); exit()
print(len(results), len(results[0]))

		
