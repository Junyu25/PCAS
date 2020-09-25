#!/usr/bin/python
from __future__ import print_function
import re,sys,os

from Bio import SeqIO
#requirement: biopython

#usage: Split_fasta_base_on_domain.py input_full_aligned_fasta (The full-aligned fa from SILVA, must be unzipped)
#output format are fixed and in the local folder.

f_in = sys.argv[1]
f = open(f_in, "r")
Bacteria = open("Bacteria.fasta", "w")
Eukaryota = open("Eukaryota.fasta", "w")
Archaea = open("Archaea.fasta", "w")
Other = open("Others.fasta", "w")

for seq_record in SeqIO.parse(f,"fasta"):
    seq = str(seq_record.seq)
    reseq = seq.replace("U", "T").replace(".", "-")
    desc = seq_record.description.split(" ")
    domain = desc[1].split(";")
    if domain[0] == "Bacteria":
        Bacteria.write(">"+str(seq_record.description)+"\n"+str(reseq)+"\n")
    elif domain[0] == "Eukaryota":
        Eukaryota.write(">"+str(seq_record.description)+"\n"+str(reseq)+"\n")
    elif domain[0] == "Archaea":
        Archaea.write(">"+str(seq_record.description)+"\n"+str(reseq)+"\n")
    else:
        Other.write(">"+str(seq_record.description)+"\n"+str(reseq)+"\n")  
        

f.close()        
Bacteria.close()
Eukaryota.close()
Archaea.close()
Other.close()