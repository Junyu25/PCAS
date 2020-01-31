#!/usr/bin/python
from __future__ import print_function
import re,sys,os

#the output is current folder
tempfilename = os.path.split(sys.argv[1])[1]
outfa = open('%s.fa' % tempfilename, 'w')
outtax = open('%s.tax' % tempfilename, 'w')

Counter=0

with open(sys.argv[1]) as infile:
	for i in infile:
		if re.match('>', i):
			isplit = i.rstrip().split(' ')
			bsplit = isplit[1].split(';')
			if Counter>0:
					#put in the \n
					print ("", file = outfa)
			print (isplit[0], file = outfa)
			print ('%s\t%s' % (isplit[0].split('>')[1], ''.join(isplit[1:])), file = outtax)
			Counter+=1
		else:
			print (i.rstrip().replace("U", "T").replace(".", "-"), end='', file = outfa)

print ("", file = outfa)

outfa.close()
outtax.close()

