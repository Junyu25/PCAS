#!/usr/bin/env python

# Usage:
# python split_taxonomy_by_domain.py  A X Y Z
# where A is the original raw SILVA taxonomy (tab separated seq ID<tab>semicolon separated taxonomy 
# X is the input taxonomy mapping file (e.g. consensus/majority, or other parsed taxonomy file)
# Y is the output 16S mapping file, Z is the output 18S mapping file.

from sys import argv

raw_taxa = open(argv[1], "U")
input_taxa = open(argv[2], "U")

output_bact_arch = open(argv[3], "w")
output_euks = open(argv[4], "w")


euk = []
bact_arch = []
for line in raw_taxa:
    if len(line.strip()) == 0:
        continue
    curr_id = line.split('\t')[0]
    curr_taxa = line.split('\t')[1].split(';')[0]
    if curr_taxa == "Eukaryota":
        euk.append(curr_id)
    elif curr_taxa in ['Bacteria', 'Archaea']:
        bact_arch.append(curr_id)
    else:
        print("Found unknown taxonomy: %s" % line.strip())

euk = set(euk)
bact_arch = set(bact_arch)

# Should be able to handle different forms of taxonomy mapping file by searching
# for Eukaryota at the beginning of the taxonomy strings
for line in input_taxa:
    curr_id = line.split()[0]
    if curr_id in euk:
        output_euks.write(line)
    elif curr_id in bact_arch:
        output_bact_arch.write(line)
    else:
        print("Non-matching ID found in input taxonomy file %s " % curr_id)
