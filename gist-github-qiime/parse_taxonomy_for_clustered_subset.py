#!/usr/bin/env python

# Usage:
# python parse_taxonomy_for_clustered_subset.py  X Y Z
# where X is the fasta file to read target labels from, Y is the taxonomy mapping file starting with a superset of labels from X, and Z is the output taxonomy mapping file.
from cogent.parse.fasta import MinimalFastaParser

from sys import argv

target_ids = []

target_fasta = open(argv[1], "U")
taxonomy_mapping = open(argv[2], "U")
taxonomy_outf = open(argv[3], "w")

for label,seq in MinimalFastaParser(target_fasta):
    target_ids.append(label.strip())

target_ids = set(target_ids)

for line in taxonomy_mapping:
    curr_id = line.split()[0]
    if curr_id in target_ids:
        taxonomy_outf.write(line)