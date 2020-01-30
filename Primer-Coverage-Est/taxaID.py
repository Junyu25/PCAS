# -*- coding: utf-8 -*-
"""
Created on Thu Sep 19 15:23:47 2019

#Extract the ID and taxa information from the original full align fasta file.

#Usage:
#python taxaID.py file.fasta 

#Input file: full align fasta file e.g. SILVA_132_LSURef_tax_silva_trunc.fasta
#Output file: file.fasta.csv which contains the ID and taxa columns


@author: Junyu
"""

import sys
import pandas as pd
from Bio import SeqIO
file = sys.argv[1]
print(file)


f = pd.DataFrame()
seqdict = {}
for seq in SeqIO.parse(file, "fasta"):
    f = f.append({'ID':seq.id, "taxa":seq.description}, ignore_index=True)

f.to_csv(file +".csv", encoding = "utf-8")