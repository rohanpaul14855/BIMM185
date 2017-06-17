'''
Convert arrowhead domainlists to .bed files
with the format chr \t start \t stop
'''

import os
import csv
from os.path import isfile, join

#get only files not directories
files = [join('data/looplist', k) for k in os.listdir('data/looplist/')]

for file in files:
    cols = []
    cl = file.split("_")[1]


    outfile = 'data/bedfiles/' + cl + ".left.bed"
    with open(file, 'r') as f:
        for entry in f:
            entry = entry.split("\t")
            cols.append(['chr' + entry[0], entry[1], entry[2]])
    with open(outfile, "w") as out:
        csv.writer(out, delimiter='\t').writerows(cols)


    outfile = 'data/bedfiles/' + cl + ".right.bed"
    with open(file, 'r') as f:
        next(f)
        for entry in f:
            entry = entry.split("\t")
            cols.append(['chr' + entry[3], entry[4], entry[5]])
    with open(outfile, "w") as out:
        csv.writer(out, delimiter='\t').writerows(cols)

