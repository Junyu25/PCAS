#!/usr/bin/env python

# Usage: python find_all_gap_positions.py X Y
# where X is the input aligned fasta file, Y is the output text file for gap
# non gapped positions

from sys import argv

from cogent.parse.fasta import MinimalFastaParser

fasta = open(argv[1], "U")

# Initialize empty array, will become 1 in positions if non gap characters
# are detected in any sequence in the alignment
# This is set to 50000 base pairs to match the Silva alignment, it can be lowered to match the length of other alignments.
alignment_positions = ['0']*50000

gap_chars = set(['.', '-'])

for label,seq in MinimalFastaParser(fasta):
    for n in range(len(seq)):
        if seq[n] in gap_chars:
            continue
        else:
            alignment_positions[n] = '1'
            
output_lanemask = open(argv[2], "w")

output_lanemask.write("%s" % "".join(alignment_positions))