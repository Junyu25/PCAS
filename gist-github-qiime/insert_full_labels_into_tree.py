#!/usr/bin/env python

""" Usage:
python insert_full_labels_into_tree.py X Y Z A
where X is the input tree file, Y is the input taxonomy mapping file (QIIME format),
and Z is the output tree file, and A is the taxa depth to parse out into the tree, e.g. 2 for domain/phylum """

from sys import argv

from cogent import LoadTree


tree_f = argv[1]

taxa_f = open(argv[2], "U")

output_tree = argv[3] 

taxa_depth = int(argv[4])


labels_map = {}
for line in taxa_f:
    curr_label = line.split('\t')[0]
    # Need to remove a number of characters that can interfere with tree loading/display
    curr_taxa = ".".join((line.split('\t')[1].split(';')[0:taxa_depth])).replace(' ','').replace('(','').replace(')','').replace(':','').replace("'", '').replace('#','')
    labels_map[curr_label] = curr_taxa

tr = LoadTree(tree_f)
tips = tr.tips()

for curr_tip in tips:
    curr_name = curr_tip.Name.replace(';', '')
    curr_tip.Name="%s;" % labels_map[curr_name]
    
tr.writeToFile(output_tree)
