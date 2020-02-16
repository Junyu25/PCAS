#!/usr/bin/python
from __future__ import print_function
import re,sys,os
from Bio import SeqIO
#This script is for checking whether the lenght of seqs in the aligned database are the same

Efa = open('database_len_summary.txt', 'w')
# Etax = open('Eukaryota.tax', 'w')
# Bfa = open('Bacteria.fa', 'w')
# Btax = open('Bacteria.tax', 'w')
# Afa = open('Archaea.fa', 'w')
# Atax = open('Archaea.tax', 'w')
'''
with open(sys.argv[1]) as infile:
	for i in infile:
		if re.match('>', i):
			isplit = str(i.rstrip())
		else:
			str_length = str(len(i.rstrip()))
			#print str_length
			print (isplit+" "+str_length, file = Efa)
'''		
file = sys.argv[1]	
for seq in SeqIO.parse(file, "fasta"):
	print (seq.id+" "+str(len(seq)), file = Efa)


Efa.close()
# Etax.close()
# Bfa.close()
# Btax.close()
# Afa.close()
# Atax.close()

#print(Ecounter)
#print(Bcounter)
#print(Acounter)