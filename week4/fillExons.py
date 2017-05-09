'''
This script is used to parse genbank files into a tab separate file
The following fields are extracted for the two genomes:
Exon start
Exon end
Length
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
            source = record.features[0].qualifiers.get('db_xref')[0].split(':')[-1]
            for feature in record.features:
                row = []
                #Get only the coding sequences
                if feature.type == 'CDS':
                    gene_id += 1
                    #Get the protein ID
                    protein_id = '-'
                    try:
                        length = len(feature.qualifiers.get('translation')[0])*3
                    except:
                        length = 0
                    num_exons = 1
                    if feature.qualifiers.get('protein_id') is not None:
                        protein_id = feature.qualifiers.get('protein_id')
                    row.append(','.join(protein_id))
                    #Get all locations
                    loc = feature.location
                    if type(loc) == Bio.SeqFeature.CompoundLocation:
                        multilocs = []
                        for i, part in enumerate(loc.parts):
                            locs = re.findall(r"[0-9]+", str(part))
                            multilocs.append(locs)
                        multilocs = ['({}, {})'.format(k[0], k[1]) for k in multilocs]
                    else:
                        start = int(loc.start)
                        stop = int(loc.end)
                        multilocs = ['({}, {})'.format(start, stop)]
                    left = ','.join([k.split(',')[0][1:] for k in multilocs])
                    right = ','.join([k.split(',')[1][:-1] for k in multilocs])
                    out.append([str(gene_id), '1', left, right, str(length)])


#Write to file
with open('exons.txt', 'w') as f:
    csv.writer(f, delimiter='\t').writerows(out)
    


