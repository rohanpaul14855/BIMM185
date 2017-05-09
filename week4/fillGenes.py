'''
This script is used to parse genbank files into a tab separate file
The following fields are extracted for the two genomes
+-------------+-----------------------+------+-----+---------+
| Field       | Type                  | Null | Key | Default |
+-------------+-----------------------+------+-----+---------+
| gene_id     | int(10) unsigned      | NO   | PRI | NULL    |
| genome_id   | int(10) unsigned      | NO   | MUL | NULL    |
| replicon_id | int(10) unsigned      | NO   | MUL | NULL    |
| locus_tag   | char(25)              | NO   | MUL | NULL    |
| protein_id  | char(25)              | NO   | MUL | NULL    |
| name        | char(10)              | NO   |     | NULL    |
| strand      | enum('F','R')         | NO   |     | NULL    |
| num_exons   | smallint(5) unsigned  | NO   |     | NULL    |
| length      | mediumint(7) unsigned | NO   |     | NULL    |
| product     | varchar(1024)         | NO   |     | NULL    |
+-------------+-----------------------+------+-----+---------+
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
            # record = SeqIO.read(f, 'genbank')
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
                    row.append(','.join(multilocs))

                    #Get the strand
                    strand = feature.location.strand
                    strand = 'F' if strand == 1 else "R"


                    #Get the gene name
                    gene_name = '-'
                    if feature.qualifiers.get('gene') is not None:
                        gene_name = feature.qualifiers.get('gene')[0]
                    row.append(gene_name)

                    #Get the locus tag
                    locus_tag = '-'
                    if feature.qualifiers.get('locus_tag') is not None:
                        locus_tag = feature.qualifiers.get('locus_tag')
                    row.append(','.join(locus_tag))

                    #Get synonyms of the gene
                    synonymous = '-'
                    if feature.qualifiers.get('gene_synonym') is not None:
                        synonymous = feature.qualifiers.get('gene_synonym')[0][1:-1].split('; ')
                    row.append(','.join(synonymous))

                    #Get the protein name, if not available, annotate as pseudo gene
                    protein_name = 'pseudo'
                    if feature.qualifiers.get('product') is not None:
                        protein_name = feature.qualifiers.get('product')


                    #Get the EC Numbers
                    EC_numbers = '-'
                    if feature.qualifiers.get('EC_number') is not None:
                        EC_numbers = feature.qualifiers.get('EC_number')[0]
                    row.append(','.join(EC_numbers))

                    #Get external references
                    # erefs = [k.split(':')[1] for k in feature.qualifiers.get('db_xref')]
                    # row.append(','.join(erefs))
                    # taxid = source
                    # row.append(taxid)
                    out.append([gene_id, genome_id, replicon_id,
                                ','.join(locus_tag), ','.join(protein_name),
                                gene_name, strand, num_exons, length,
                                ','.join(protein_name)])
        genome_id += 1            # out.append(row)

#Write to file
with open('genes2.txt', 'w') as f:
    csv.writer(f, delimiter='\t').writerows(out)
    


