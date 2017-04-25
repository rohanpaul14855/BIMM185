'''
This script is used to parse genbank files into a tab separate file
The following fields are extracted
Tax ID
the accession
coordinates
strand
gene name
locus tag
synonyms
protein name
EC-number(s)
external references
'''


from Bio import SeqIO
import gzip
import csv
import Bio
import re


#Master list to store all values with header
out = [['Tax ID', 'Accession Numbers', 'Coordinates', 'Strand', 'Gene Name', 'Locus Tag',
        'Synonyms', 'Protein Name', 'EC-Numbers', 'External References']]

#Open file using the gzip module to read without first unzipping
with gzip.open('GCF_000005845.2_ASM584v2_genomic.gbff.gz', 'rt') as f:
    record = SeqIO.read(f, 'genbank')
    source = record.features[0].qualifiers.get('db_xref')[0].split(':')[-1]
    for feature in record.features:
        row = []
        #Get only the coding sequences
        if feature.type == 'CDS':
            #Get the protein ID
            protein_id = '-'
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
            row.append(strand)

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
            row.append(','.join(protein_name))

            #Get the EC Numbers
            EC_numbers = '-'
            if feature.qualifiers.get('EC_number') is not None:
                EC_numbers = feature.qualifiers.get('EC_number')[0]
            row.append(','.join(EC_numbers))

            #Get external references
            erefs = [k.split(':')[1] for k in feature.qualifiers.get('db_xref')]
            row.append(','.join(erefs))
            taxid = source
            row.append(taxid)
            out.append(row)

#Write to file
with open('EColi.tsv', 'w') as f:
    writer = csv.writer(f, delimiter='\t')
    writer.writerows(out)
    


