# -*- coding: utf-8 -*-
"""
Usage:
    Python Amplicon-Analysis.py file.fasta
"""
#import numpy as np
import sys
import pylab
import numpy as np
import pandas as pd
from Bio import SeqIO
file = sys.argv[1]
print(file)

sizes = [len(rec) for rec in SeqIO.parse(file , "fasta")]
#%pylab inline
#%matplotlib inline
pylab.hist(sizes, bins=20)
pylab.title("%i sequences\nLengths %i to %i" \
            % (len(sizes),min(sizes),max(sizes)))
pylab.xlabel("Sequence length (bp)")
pylab.ylabel("Count")
#pylab.show()

pylab.savefig(file+".png")
pylab.savefig(file+".pdf")

mean = sum(sizes)/len(sizes)
#lenrange = max(sizes)-min(sizes)
percent = np.percentile(sizes, [10, 20, 30, 40, 50, 60, 70, 80, 90,])

sta= open("Output.txt","w")
sta.write("10% is: "+ str(percent[0]) +"\n" \
          "20% is: "+ str(percent[1]) +"\n" \
          "30% is: "+ str(percent[2]) +"\n" \
          "40% is: "+ str(percent[3]) +"\n" \
          "50% is: "+ str(percent[4]) +"\n" \
          "60% is: "+ str(percent[5]) +"\n" \
          "70% is: "+ str(percent[6]) +"\n" \
          "80% is: "+ str(percent[7]) +"\n" \
          "90% is: "+ str(percent[8]) +"\n\n" \
          
          
          "Min length is:" + str(min(sizes))+"\n" \
          "mean is: "+ str(mean) +"\n" \
          "Max length is:" + str(max(sizes))+"\n" \
        
          )
sta.close() 


f = pd.DataFrame()
seqdict = {}
for seq_record in SeqIO.parse(file, "fasta"):
    f = f.append({'ID':seq_record.id, "Len":len(seq_record)}, ignore_index=True)

sort_by_len = f.sort_values('Len')
#print(sort_by_len.head(n=3))
sort_by_len.to_csv(file +".csv", encoding = "utf-8")

