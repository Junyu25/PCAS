#!/usr/bin/env python

""" Usage:
python split_sequences_by_domain.py input_taxa_file input_fasta_to_split output_16S_fasta output_18S_fasta
"""

from sys import argv

from cogent.parse.fasta import MinimalFastaParser

input_taxa = open(argv[1], "U")
input_fasta = open(argv[2], "U")

output_bact_arch = open(argv[3], "w")
output_euks = open(argv[4], "w")

euk_string = "Eukaryota"
bact_string = "Bacteria"
arch_string = "Archaea"

# Should be able to handle different forms of taxonomy mapping file by searching
# for Eukaryota at the beginning of the taxonomy strings
euk_ids = []
for line in input_taxa:
    curr_taxa = line.split()[1][0:15]
    if euk_string in curr_taxa:
        euk_ids.append(line.split()[0])
    # Need to test to make sure shows up in Bacteria or Archaea
    else:
        if bact_string not in curr_taxa and arch_string not in curr_taxa:
            raise ValueError,("Eukaryota, Bacteria, and Archaea not found "+\
                "in taxa string %s" % curr_taxa)

euk_ids = set(euk_ids)

for label,seq in MinimalFastaParser(input_fasta):
    if label in euk_ids:
        output_euks.write(">%s\n%s\n" % (label, seq))
    else:
        output_bact_arch.write(">%s\n%s\n" % (label, seq))

