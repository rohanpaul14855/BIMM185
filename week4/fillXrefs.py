'''
This script is used to parse genbank files into a tab separate file
The following fields are extracted for the two genomes
external databases
external database ID
'''


from Bio import SeqIO
import gzip
import csv
import Bio
import re

out = []
files = ['../week3/GCF_000005845.2_ASM584v2_genomic.gbff.gz', 'GCF_000576515.1_ASM57651v1_genomic.gbff.gz']

genome_id = 1
replicon_id = 0
gene_id = 0

#Open file using the gzip module to read without first unzipping
for file in files:
    with gzip.open(file, 'rt') as f:
        for record in SeqIO.parse(f, 'genbank'):
            replicon_id +=1
            source = record.features[0].qualifiers.get('db_xref')[0].split(':')[-1]
            for feature in record.features:
                row = []
                #Get only the coding sequences
                if feature.type == 'CDS':
                    pid = feature.qualifiers.get('protein_id')
                    if pid is not None:
                        pid = pid[0].split('.')[0]
                        pdb = 'refseq'
                    xrefs = feature.qualifiers.get('db_xref')
                    gene_id += 1
                    if pid is not None:
                        out.append([gene_id, pdb, pid])
                    try:
                        for db, refid in [k.split(':') for k in xrefs]:
                            if "swiss" in db.lower():
                                db = 'uniprot'
                            out.append([gene_id, db.lower(), refid])
                    except TypeError: #some genes may not have
                        out.append([gene_id, '-', '-'])


#Write to file
with open('xrefs2.txt', 'w') as f:
    csv.writer(f, delimiter='\t').writerows(out)
    


