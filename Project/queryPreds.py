import MySQLdb
'''
Used to query SQL table containing predictions on the single cell line
'''

sqldb = MySQLdb.connect(host="bm185s-mysql.ucsd.edu", user="bm185sag", passwd="Arturo!*", db="bm185sag_db")
cur = sqldb.cursor()

cells = ['HeLa', 'HMEC', 'HUVEC', 'K562', 'NHEK']

for cell in cells:
	correct = 0
	incorrect = 0
	cur.execute('SELECT * FROM predictions WHERE cell="{}";'.format(cell))
	for row in cur.fetchall():
		if row[-1] == row[-2]:
			correct += 1	
		else:
			incorrect +=1
	print(cell, correct, incorrect)
