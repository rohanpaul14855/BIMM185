from Bio import SeqIO
import numpy as np
import gzip
import csv

files = ['../week3/GCF_000005845.2_ASM584v2_genomic.gbff.gz', 'GCF_000576515.1_ASM57651v1_genomic.gbff.gz']
out = []
genome_id = 0
for infile in files:
    genome_id += 1
    with gzip.open(infile, 'rt') as f:
        length = 0
        num_replicons = 0
        num_genes = 0

        for record in SeqIO.parse(f, 'genbank'):
            name = record.annotations.get('organism')
            fname = infile.split('/')[-1]
            assembly = '_'.join(fname.split('_')[:2]).split('.')[0]
            num_replicons += 1
            acc = record.name
            # name = record.description
            length += len(record.seq)
            domain = record.annotations.get('taxonomy')[0]
            for feature in record.features:
                if feature.type == 'CDS':
                    num_genes +=1
            if domain == 'Bacteria':
                domain = 'bacteria'
            elif domain == 'Eukaryota':
                domain = 'eukarya'
            elif domain == 'Archaeon':
                domain = 'archea'
            else:
                print(domain)
                exit('unrecognized domain')
            taxid = record.features[0].qualifiers.get('db_xref')[0].split(':')[1]
        out.append([genome_id, name, taxid, domain,
                    num_replicons, num_genes, length,
                    assembly])

with open('genomes2.txt', 'w') as f:
    csv.writer(f, delimiter='\t').writerows(out)

print(np.array(out))
