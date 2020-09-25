#!/usr/bin/python
from __future__ import print_function
from __future__ import division
import re,sys,os
import json

#   Copyright {2019} Yuxiang Tan
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

#This script will read in the ID_merge_tax of a primer and do the primer coverage analysis

#This script starts from The _ID.txt_merge_taxa.txt (such as 515Yf_ID.txt_merge_taxa.txt)
#Library file requirement: python 2.7 and up

#Usage: python primer_taxa_coverage_calculator.py ID_merge_tax database_summary_folder output_folder

input_ID = sys.argv[1]
database_sum = sys.argv[2]
out_folder = sys.argv[3]

#########check files and folders  
if not os.path.isfile(input_ID):
    print('Input ID merge tax file %s is not exist; Exit now.' % input_ID)
    exit(0)

if not os.path.exists(database_sum):
    print('The database summary folder %s is not exist; Exit now.' % database_sum)
    exit(0)

if not os.path.exists(out_folder):
    os.mkdir(out_folder)



#species dic
D0_sp={}
D1_sp={}
D2_sp={}
D3_sp={}
D4_sp={}
D5_sp={}
D6_sp={}

#strain dic
D0_str={}
D1_str={}
D2_str={}
D3_str={}
D4_str={}
D5_str={}
D6_str={}


with open(input_ID) as infile:
    for i in infile:
        isplit = i.rstrip().split(' ')
        bsplit = isplit[1].split(';')
        len_tax=len(bsplit)
        #deal with tax with different levels, the 7-level rule was applied
        if len_tax==7:
            D0_index=bsplit[0]
            D1_index=";".join(bsplit[0:2])
            D2_index=";".join(bsplit[0:3])
            D3_index=";".join(bsplit[0:4])
            D4_index=";".join(bsplit[0:5])
            D5_index=";".join(bsplit[0:6])
            D6_str_index=";".join(bsplit[0:6])+"_"+bsplit[6]
            sp_split= bsplit[6].split('::')
            D6_sp_index=";".join(bsplit[0:6])+"_"+sp_split[0]
        elif len_tax>7:
            D0_index=bsplit[0]
            D1_index=";".join(bsplit[0:2])
            D2_index=";".join(bsplit[0:3])
            D3_index=";".join(bsplit[0:4])
            D4_index=";".join(bsplit[0:5])
            D5_index=";".join(bsplit[0:6])
            D6_str_index=";".join(bsplit[0:6])+"_"+"_".join(bsplit[6:])
            sp_split= bsplit[len_tax-1].split('::')
            D6_sp_index=";".join(bsplit[0:6])+"_"+"_".join(bsplit[6:-1])+"_"+sp_split[0]
        else:
            index_count=0
            index_list=[]
            for index_count in range(0,6):
                if index_count<(len_tax-1):
                    index_list.append(";".join(bsplit[0:(index_count+1)]))
                elif index_count==(len_tax-1):
                    sp_split= bsplit[len_tax-1].split('::')
                    index_list.append(";".join(bsplit[0:(index_count)])+";"+sp_split[0])
                else:
                    index_list.append(index_list[index_count-1]+";"+"NA")
            index_list.append(index_list[5]+"_"+"NA")
            D0_index=index_list[0]
            D1_index=index_list[1]
            D2_index=index_list[2]
            D3_index=index_list[3]
            D4_index=index_list[4]
            D5_index=index_list[5]
            D6_str_index="::".join([index_list[6],sp_split[1]])
            D6_sp_index=index_list[6]
        
        #assign into the dictionary, and check whether a strain has duplicate
        if D6_sp_index in D6_sp:
            if D6_str_index in D6_str:
                print('warning: the input taxa file has duplicated strains, please check to avoid mistake. Ignore it now.')
            else:
                D0_str[D0_index]+=1
                D1_str[D1_index]+=1
                D2_str[D2_index]+=1
                D3_str[D3_index]+=1
                D4_str[D4_index]+=1
                D5_str[D5_index]+=1
                D6_str[D6_str_index]=1
                D6_sp[D6_sp_index]+=1
        else:
            if D0_index in D0_str:
                D0_str[D0_index]+=1
                D0_sp[D0_index]+=1
            else:
                D0_str[D0_index]=1
                D0_sp[D0_index]=1
            
            if D1_index in D1_str:
                D1_str[D1_index]+=1
                D1_sp[D1_index]+=1
            else:
                D1_str[D1_index]=1
                D1_sp[D1_index]=1
            
            if D2_index in D2_str:
                D2_str[D2_index]+=1
                D2_sp[D2_index]+=1
            else:
                D2_str[D2_index]=1
                D2_sp[D2_index]=1
            
            if D3_index in D3_str:
                D3_str[D3_index]+=1
                D3_sp[D3_index]+=1
            else:
                D3_str[D3_index]=1
                D3_sp[D3_index]=1
            
            if D4_index in D4_str:
                D4_str[D4_index]+=1
                D4_sp[D4_index]+=1
            else:
                D4_str[D4_index]=1
                D4_sp[D4_index]=1
            
            if D5_index in D5_str:
                D5_str[D5_index]+=1
                D5_sp[D5_index]+=1
            else:
                D5_str[D5_index]=1
                D5_sp[D5_index]=1
            
            if D6_str_index in D6_str:
                print('warning: there must be a bug, if you meet it, report it.')
            else:
                D6_str[D6_str_index]=1
            D6_sp[D6_sp_index]=1
        
        


#Read the dictionaries from database_sum json files
#species dicts
file = open('%s/D0_species_dic.json' % (database_sum), 'r') 
js = file.read()
D0_sp_sum = json.loads(js)    
file.close()

file = open('%s/D1_species_dic.json' % (database_sum), 'r') 
js = file.read()
D1_sp_sum = json.loads(js)    
file.close()

file = open('%s/D2_species_dic.json' % (database_sum), 'r') 
js = file.read()
D2_sp_sum = json.loads(js)    
file.close()

file = open('%s/D3_species_dic.json' % (database_sum), 'r') 
js = file.read()
D3_sp_sum = json.loads(js)    
file.close()

file = open('%s/D4_species_dic.json' % (database_sum), 'r') 
js = file.read()
D4_sp_sum = json.loads(js)    
file.close()

file = open('%s/D5_species_dic.json' % (database_sum), 'r') 
js = file.read()
D5_sp_sum = json.loads(js)    
file.close()

file = open('%s/D6_species_dic.json' % (database_sum), 'r') 
js = file.read()
D6_sp_sum = json.loads(js)    
file.close()

#strain dic
file = open('%s/D0_strain_dic.json' % (database_sum), 'r') 
js = file.read()
D0_str_sum = json.loads(js)    
file.close()

file = open('%s/D1_strain_dic.json' % (database_sum), 'r') 
js = file.read()
D1_str_sum = json.loads(js)    
file.close()

file = open('%s/D2_strain_dic.json' % (database_sum), 'r') 
js = file.read()
D2_str_sum = json.loads(js)    
file.close()

file = open('%s/D3_strain_dic.json' % (database_sum), 'r') 
js = file.read()
D3_str_sum = json.loads(js)    
file.close()

file = open('%s/D4_strain_dic.json' % (database_sum), 'r') 
js = file.read()
D4_str_sum = json.loads(js)    
file.close()

file = open('%s/D5_strain_dic.json' % (database_sum), 'r') 
js = file.read()
D5_str_sum = json.loads(js)    
file.close()


#compare two dictionaries and generate summary reports
header_list=["taxonomy", "species_num_primer", "seq_num_primer", "species_num_bg", "seq_num_bg", "taxa-species", "unique-sequence"]

outfile = open("%s/D0_stat_all.txt_cover_percentage.txt" % (out_folder),'w')
outfile.write("\t".join(header_list)+"\n")
for D0_sp_sum_key in D0_sp_sum.keys():
    if D0_sp_sum_key not in D0_sp:
        #since sp and str has the same keys with different number, we can do it together
        species_num_primer=0
        seq_num_primer=0
    else:
        species_num_primer=D0_sp[D0_sp_sum_key]
        seq_num_primer=D0_str[D0_sp_sum_key]
    
    species_num_bg=D0_sp_sum[D0_sp_sum_key]
    seq_num_bg=D0_str_sum[D0_sp_sum_key]
    
    taxa_species=species_num_primer/species_num_bg
    unique_sequence=seq_num_primer/seq_num_bg
    
    outfile.write(D0_sp_sum_key+"\t"+str(species_num_primer)+"\t"+str(seq_num_primer)+"\t"+str(species_num_bg)+"\t"+str(seq_num_bg)+"\t"+str(taxa_species)+"\t"+str(unique_sequence)+"\n")

outfile.close()

outfile = open("%s/D1_stat_all.txt_cover_percentage.txt" % (out_folder),'w')
outfile.write("\t".join(header_list)+"\n")
for D1_sp_sum_key in D1_sp_sum.keys():
    if D1_sp_sum_key not in D1_sp:
        #since sp and str has the same keys with different number, we can do it together
        species_num_primer=0
        seq_num_primer=0
    else:
        species_num_primer=D1_sp[D1_sp_sum_key]
        seq_num_primer=D1_str[D1_sp_sum_key]
    
    species_num_bg=D1_sp_sum[D1_sp_sum_key]
    seq_num_bg=D1_str_sum[D1_sp_sum_key]
    
    taxa_species=species_num_primer/species_num_bg
    unique_sequence=seq_num_primer/seq_num_bg
    
    outfile.write(D1_sp_sum_key+"\t"+str(species_num_primer)+"\t"+str(seq_num_primer)+"\t"+str(species_num_bg)+"\t"+str(seq_num_bg)+"\t"+str(taxa_species)+"\t"+str(unique_sequence)+"\n")

outfile.close()

outfile = open("%s/D2_stat_all.txt_cover_percentage.txt" % (out_folder),'w')
outfile.write("\t".join(header_list)+"\n")
for D2_sp_sum_key in D2_sp_sum.keys():
    if D2_sp_sum_key not in D2_sp:
        #since sp and str has the same keys with different number, we can do it together
        species_num_primer=0
        seq_num_primer=0
    else:
        species_num_primer=D2_sp[D2_sp_sum_key]
        seq_num_primer=D2_str[D2_sp_sum_key]
    
    species_num_bg=D2_sp_sum[D2_sp_sum_key]
    seq_num_bg=D2_str_sum[D2_sp_sum_key]
    
    taxa_species=species_num_primer/species_num_bg
    unique_sequence=seq_num_primer/seq_num_bg
    
    outfile.write(D2_sp_sum_key+"\t"+str(species_num_primer)+"\t"+str(seq_num_primer)+"\t"+str(species_num_bg)+"\t"+str(seq_num_bg)+"\t"+str(taxa_species)+"\t"+str(unique_sequence)+"\n")

outfile.close()

outfile = open("%s/D3_stat_all.txt_cover_percentage.txt" % (out_folder),'w')
outfile.write("\t".join(header_list)+"\n")
for D3_sp_sum_key in D3_sp_sum.keys():
    if D3_sp_sum_key not in D3_sp:
        #since sp and str has the same keys with different number, we can do it together
        species_num_primer=0
        seq_num_primer=0
    else:
        species_num_primer=D3_sp[D3_sp_sum_key]
        seq_num_primer=D3_str[D3_sp_sum_key]
    
    species_num_bg=D3_sp_sum[D3_sp_sum_key]
    seq_num_bg=D3_str_sum[D3_sp_sum_key]
    
    taxa_species=species_num_primer/species_num_bg
    unique_sequence=seq_num_primer/seq_num_bg
    
    outfile.write(D3_sp_sum_key+"\t"+str(species_num_primer)+"\t"+str(seq_num_primer)+"\t"+str(species_num_bg)+"\t"+str(seq_num_bg)+"\t"+str(taxa_species)+"\t"+str(unique_sequence)+"\n")

outfile.close()

outfile = open("%s/D4_stat_all.txt_cover_percentage.txt" % (out_folder),'w')
outfile.write("\t".join(header_list)+"\n")
for D4_sp_sum_key in D4_sp_sum.keys():
    if D4_sp_sum_key not in D4_sp:
        #since sp and str has the same keys with different number, we can do it together
        species_num_primer=0
        seq_num_primer=0
    else:
        species_num_primer=D4_sp[D4_sp_sum_key]
        seq_num_primer=D4_str[D4_sp_sum_key]
    
    species_num_bg=D4_sp_sum[D4_sp_sum_key]
    seq_num_bg=D4_str_sum[D4_sp_sum_key]
    
    taxa_species=species_num_primer/species_num_bg
    unique_sequence=seq_num_primer/seq_num_bg
    
    outfile.write(D4_sp_sum_key+"\t"+str(species_num_primer)+"\t"+str(seq_num_primer)+"\t"+str(species_num_bg)+"\t"+str(seq_num_bg)+"\t"+str(taxa_species)+"\t"+str(unique_sequence)+"\n")

outfile.close()

outfile = open("%s/D5_stat_all.txt_cover_percentage.txt" % (out_folder),'w')
outfile.write("\t".join(header_list)+"\n")
for D5_sp_sum_key in D5_sp_sum.keys():
    if D5_sp_sum_key not in D5_sp:
        #since sp and str has the same keys with different number, we can do it together
        species_num_primer=0
        seq_num_primer=0
    else:
        species_num_primer=D5_sp[D5_sp_sum_key]
        seq_num_primer=D5_str[D5_sp_sum_key]
    
    species_num_bg=D5_sp_sum[D5_sp_sum_key]
    seq_num_bg=D5_str_sum[D5_sp_sum_key]
    
    taxa_species=species_num_primer/species_num_bg
    unique_sequence=seq_num_primer/seq_num_bg
    
    outfile.write(D5_sp_sum_key+"\t"+str(species_num_primer)+"\t"+str(seq_num_primer)+"\t"+str(species_num_bg)+"\t"+str(seq_num_bg)+"\t"+str(taxa_species)+"\t"+str(unique_sequence)+"\n")

outfile.close()

outfile = open("%s/D6_stat_all.txt_cover_percentage.txt" % (out_folder),'w')
outfile.write("\t".join(header_list)+"\n")
#because this level is the last level, use only the species dic.
for D6_sp_sum_key in D6_sp_sum.keys():
    #because this level has additional str info in the key, as a result, need to process differently
    if D6_sp_sum_key not in D6_sp:
        #since sp and str has the same keys with different number, we can do it together
        species_num_primer=0
        seq_num_primer=0
    else:
        species_num_primer=1
        seq_num_primer=D6_sp[D6_sp_sum_key]
    
    species_num_bg=1
    seq_num_bg=D6_sp_sum[D6_sp_sum_key]
    
    taxa_species=species_num_primer/species_num_bg
    unique_sequence=seq_num_primer/seq_num_bg
    
    outfile.write(D6_sp_sum_key+"\t"+str(species_num_primer)+"\t"+str(seq_num_primer)+"\t"+str(species_num_bg)+"\t"+str(seq_num_bg)+"\t"+str(taxa_species)+"\t"+str(unique_sequence)+"\n")

outfile.close()




