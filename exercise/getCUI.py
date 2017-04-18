"""
Calculates the codon usage index for each sequence
p = proabability of a codon in the exome
q = relative frequency of a codon in a gene
cui = sum over all codons(p * q)
"""

import pandas as pd
import itertools
import csv

df = pd.read_csv('frequencies.tsv', sep='\t', index_col=0, header=0)
totals = df.loc['Totals']
codons = [''.join(i) for i in itertools.product(['A', 'T', 'C', 'G'], repeat = 3)]

cui = [['Locus', 'CUI']]
for index, row in df.iterrows():
    if index == 'Totals': 
        continue
    row_cui = 0
    for codon in codons:
        q = row[codon]/row['Length']
        p = totals[codon]/totals['Length']
        row_cui += (p*q)
    cui.append([index, "%.4f" % row_cui])

with open('cui.txt', 'w') as f:
    writer = csv.writer(f, delimiter='\t')
    writer.writerows(cui)





