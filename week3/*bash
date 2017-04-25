#!/usr/bin/env bash

#Downloads README file from uniprot and downloads information for three bacteria

#wget ftp://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/reference_proteomes/README

for i in UP000034024 UP000050566  UP000029777; do
    wget -P ${i} ftp://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/reference_proteomes/Bacteria/${i}_*
done