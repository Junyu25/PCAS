#!/usr/bin/env python

from sys import argv
from cogent.parse.fasta import MinimalFastaParser

input_f = open(argv[1], "U")
output_f = open(argv[2], "w")

for label,seq in MinimalFastaParser(input_f):
    curr_label = label.split()[0]
    output_f.write(">%s\n%s\n" %(curr_label, seq))