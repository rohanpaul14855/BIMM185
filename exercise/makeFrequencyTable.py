'''
Creates tsv file with counts for each codon in each gene
Also stores length (in codons) of each gene and totals for each column
'''

import pandas as pd
import itertools

#Create all permutations of 'ATGC' of length 3
codons = [''.join(i) for i in itertools.product(['A', 'T', 'C', 'G'], repeat = 3)]
codons += ['Length' , 'Locus']
with open('cds.tsv', 'r') as f:
    data = [k.split('\t') for k in f]

freq = []
for line in data:
    freqs = {k: 0 for k in codons}
    locus = line[0].strip()
    seq = line[1].strip()
    freqs['Length'] = len(seq)/3
    freqs['Locus'] = locus
    for i in range(0, len(seq), 3):
        try:
            freqs[seq[i:i+3]] += 1
        except:
            #not a triplet
            print(locus, len(seq))
            continue
    freq.append(freqs)    
        


df = pd.DataFrame(freq)
df.set_index('Locus', inplace=True)
totals = df.sum().rename('Totals')
df = df.append(totals).astype(int)
df.to_csv('frequencies.tsv', sep='\t')




         



