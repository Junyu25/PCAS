# -*- coding: utf-8 -*-
"""
Created on Mon Sep 23 11:11:12 2019

@author: Junyu
"""

import os
from Bio import SeqIO
#import full-allign fasta
f = open("Ecoli.K-12substr.MG1655.fa", "r")
Ecoli = open("Ecoli.K-12substr.MG1655.fasta", "w")

record = SeqIO.read("Ecoli.K-12substr.MG1655.fa", "fasta")
seq = str(record.seq)
reseq = seq.replace("U", "T").replace("-", "")
    
Ecoli.write(">"+str(record.description)+"\n"+str(reseq))

f.close()        
Ecoli.close()

primer = SeqIO.read("demo.fasta", "fasta")

analyze_primers = "analyze_primers.py -f "+str("Ecoli.K-12substr.MG1655.fasta")+" -p "+str(primer.id)+" -s "+str(primer)
os.system(analyze_primers)

hits = primer.id+"_hits.txt"


get_amplicons = "get_amplicons_and_reads.py -f "+str("Ecoli.K-12substr.MG1655.fasta")+" -i "+str(hits)+" -R 250 -o ./Arc"
os.system(get_amplicons)

amplicon = SeqIO.read(primer.id+"_amplicons.fasta", "fasta")
standerlen = len(amplicon)
