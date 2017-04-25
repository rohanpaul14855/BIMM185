'''
Reads the protein sequence fasta file for EColi
Then writes protein id \t sequence to file
'''

import gzip
from Bio import SeqIO
import csv

out = []
with gzip.open('GCF_000005845.2_ASM584v2_protein.faa.gz', 'rt') as f:
    for record in SeqIO.parse(f, "fasta"):
        protein_id = '-'
        if record.id is not None:
            protein_id = record.id
        seq = '-'
        if record.seq is not None:
            seq = record.seq
        out.append([protein_id, seq])

with open('EColi_protein_sequences.txt', 'w') as f:
    csv.writer(f, delimiter='\t').writerows(out)

