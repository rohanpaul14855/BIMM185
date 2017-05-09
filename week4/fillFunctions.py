'''
This script is used to parse genbank files into a tab separate file
The following fields are extracted for the two genomes:
function
'''


from Bio import SeqIO
import gzip
import csv
import Bio
import re


#Master list to store all values with header
# out = [['Tax ID', 'Accession Numbers', 'Coordinates', 'Strand', 'Gene Name', 'Locus Tag',
#         'Synonyms', 'Protein Name', 'EC-Numbers', 'External References']]
out = []
files = ['../week3/GCF_000005845.2_ASM584v2_genomic.gbff.gz', 'GCF_000576515.1_ASM57651v1_genomic.gbff.gz']

genome_id = 1
replicon_id = 0
gene_id = 0

#Open file using the gzip module to read without first unzipping
for file in files:
    with gzip.open(file, 'rt') as f:
        for record in SeqIO.parse(f, 'genbank'):
            # record = SeqIO.read(f, 'genbank')
            source = record.features[0].qualifiers.get('db_xref')[0].split(':')[-1]
            for feature in record.features:
                row = []
                #Get only the coding sequences
                if feature.type == 'CDS':
                    print(feature)
                    gene_id += 1
                    #Get the protein ID
                    function = '-'
                    if feature.qualifiers.get('function') is not None:
                        function  = feature.qualifiers.get('function')[0]
                    print(function)

                    out.append([gene_id, function])
#Write to file
with open('functions.txt', 'w') as f:
    csv.writer(f, delimiter='\t').writerows(out)
    


