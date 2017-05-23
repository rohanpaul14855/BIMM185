import csv

# columns = ['gene_id', '']
# genes = pd.read_csv('../week4/genes.txt', sep='\t', header=0)
# print(genes.columns)

with open('../week4/genes.txt', 'r') as f:
    genes = list(csv.reader(f, delimiter='\t'))

out = []
with open('strongOrConfirmedOperons.txt', 'r') as f:
    operons = csv.reader(f, delimiter='\t')
    for line in operons:
        gene_names = line[1].split(',')
        ltags = []
        for name in gene_names:
            for line2 in genes:
                if line2[5] == name:
                    ltags.append(line2[3])
        out.append([line[0]] + [','.join(ltags)] + [line[2]])

with open('strongOrConfirmedOperons.ltags.txt', 'w') as f:
    csv.writer(f, delimiter='\t').writerows(out)


