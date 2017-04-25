'''
Parses uniprot file and creates a tab separated table
with the taxid, organism and taxonomy for each entry
'''

from Bio import SwissProt
import gzip
import csv

out = []
with gzip.open('uniprot_sprot_archaea.dat.gz', 'rt') as f:
    for record in SwissProt.parse(f):
        taxid = record.taxonomy_id
        organism = record.organism
        taxonomy = record.organism_classification
        out.append([','.join(taxid), organism, ','.join(taxonomy)])

with open('EColi_uniprot.txt', 'w') as f:
    csv.writer(f, delimiter='\t').writerows(out)