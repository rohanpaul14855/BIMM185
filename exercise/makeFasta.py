'''
generates a fasta file with all coding sequences of E. Coli genome
gets start and stop coordinates from ProteinTable167_161521 (1).txt
gets sequence from 'GCF_000005845.2_ASM584v2_genomic.fna'
reverse complements those sequences that are on the reverse strand
'''


import pandas as pd

with open('GCF_000005845.2_ASM584v2_genomic.fna', 'r') as f:
    next(f)
    genome = ''.join([k.strip() for k in f.readlines() if not k[0] == '>'])

df = pd.read_csv('ProteinTable167_161521 (1).txt', sep='\t', index_col=0, header=0)


def revcomp(string):
    rev = ''
    for letter in string:
        if letter == 'A':
            rev += 'T'
        if letter == 'T':
            rev += 'A'
        if letter == 'C':
            rev += 'G'
        if letter == 'G':
            rev += 'C'
    return rev[::-1]



with open('cds.fa', 'w') as f:
    for index, row in df.iterrows():
        ids = '>' + row['Protein product'] + '|' + row['Locus'] + '|' + row['Locus tag']
        start = int(row['Start']) - 1
        stop = int(row['Stop'])
        seq = genome[start: stop]
        if row['Strand'] == '-':
            seq = revcomp(seq)
        f.write(ids)
        f.write('\n')
        for i in range(0, len(seq), 70):
            f.write(seq[i: i+70])
            f.write('\n')









