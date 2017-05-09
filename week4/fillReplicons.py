'''
This script is used to parse genbank files into a tab separate file
The following fields are extracted for the two genomes
+--------------+------------------------------+------+-----+---------+
| Field        | Type                         | Null | Key | Default |
+--------------+------------------------------+------+-----+---------+
| replicon_id  | int(10) unsigned             | NO   | PRI | NULL    |
| genome_id    | int(10) unsigned             | NO   | MUL | NULL    |
| name         | varchar(256)                 | NO   |     | NULL    |
| type         | enum('chromosome','plasmid') | NO   |     | NULL    |
| shape        | enum('circular','linear')    | NO   |     | NULL    |
| num_genes    | int(10) unsigned             | NO   |     | NULL    |
| size_bp      | bigint(15) unsigned          | NO   |     | NULL    |
| accession    | varchar(25)                  | NO   |     | NULL    |
| release_date | varchar(25)                  | NO   |     | NULL    |
+--------------+------------------------------+------+-----+---------+

'''

from Bio import SeqIO
import numpy as np
import gzip
import csv

files = ['../week3/GCF_000005845.2_ASM584v2_genomic.gbff.gz', 'GCF_000576515.1_ASM57651v1_genomic.gbff.gz']
out = []
genome_id = 1
replicon_id = 0
for infile in files:
    with gzip.open(infile, 'rt') as f:
        for record in SeqIO.parse(f, 'genbank'):
            accession = record.name
            date = record.annotations.get('date')
            name = record.description
            if 'plasmid' in name.lower():
                replicon_type = 'plasmid'
            else:
                replicon_type = 'chromosome'
            name = ' '.join(record.description.split(' ')[:2])
            replicon_id += 1
            num_genes = 0
            length = len(record.seq)
            for feature in record.features:
                if feature.type == 'CDS':
                    num_genes += 1
            replicon_shape = record.annotations.get('topology')
            out.append([replicon_id, genome_id, name,
                        replicon_type, replicon_shape,
                        num_genes, length, accession, date])

    genome_id = 2

with open('replicons2.txt', 'w') as f:
    csv.writer(f, delimiter='\t').writerows(out)

print(np.array(out))
