#!/usr/bin/python
from __future__ import print_function
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

#This script will read in the uniq_tax of a database and turn it into 7 json files as dictionary for the primer coverage analysis

#This script starts from The _uniq.tax (such as SILVA_138_SSURef_tax_silva_uniq.tax)
#Library file requirement: python 2.7 and up

#Usage: python uniq_strain_tax_2_jsons.py database_tax output_folder

#########check files and folders  
if not os.path.isfile(sys.argv[1]):
    print('Input tax is not exist; Exit now.')
    exit(0)

if not os.path.exists(sys.argv[2]):
    os.mkdir(sys.argv[2])

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

#contradiction dic
D1_contr={}
D2_contr={}
D3_contr={}
D4_contr={}
D5_contr={}



out_strain_tax = open('%s_uniq_strain.tax' % (sys.argv[1].split("_uniq.tax")[0]), 'w')
with open(sys.argv[1]) as infile:
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
            D6_sp_index=";".join(bsplit[0:6])+"_"+bsplit[6]
        elif len_tax>7:
            D0_index=bsplit[0]
            D1_index=";".join(bsplit[0:2])
            D2_index=";".join(bsplit[0:3])
            D3_index=";".join(bsplit[0:4])
            D4_index=";".join(bsplit[0:5])
            D5_index=";".join(bsplit[0:6])
            D6_sp_index=";".join(bsplit[0:6])+"_"+"_".join(bsplit[6:])
        else:
            index_count=0
            index_list=[]
            for index_count in range(0,6):
                if index_count<(len_tax):
                    index_list.append(";".join(bsplit[0:(index_count+1)]))
                else:
                    index_list.append(index_list[index_count-1]+";"+"NA")
            index_list.append(index_list[5]+"_"+"NA")
            D0_index=index_list[0]
            D1_index=index_list[1]
            D2_index=index_list[2]
            D3_index=index_list[3]
            D4_index=index_list[4]
            D5_index=index_list[5]
            D6_sp_index=index_list[6]
        
        #assign into the dictionary, and check whether a strain has duplicate
        if D6_sp_index in D6_sp:
            D0_str[D0_index]+=1
            D1_str[D1_index]+=1
            D2_str[D2_index]+=1
            D3_str[D3_index]+=1
            D4_str[D4_index]+=1
            D5_str[D5_index]+=1
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
            
            D6_sp[D6_sp_index]=1
        
        #print into the strain tax
        print (i.rstrip()+"::str"+str(D6_sp[D6_sp_index])+"\n", file = out_strain_tax)
        
        #check contradiction
        contri_list = D6_sp_index.split(';')
        if contri_list[1]=="NA":
            continue
        else:
            if contri_list[1] in D1_contr:
                if contri_list[0] in D1_contr[contri_list[1]]:
                    D1_contr[contri_list[1]][contri_list[0]].append(isplit[0])
                else:
                    D1_contr[contri_list[1]][contri_list[0]]=[isplit[0]]
                
            else:
                D1_contr[contri_list[1]]={}
                D1_contr[contri_list[1]][contri_list[0]]=[isplit[0]]
        
        contri_lv2 = ";".join(contri_list[0:2])
        if contri_list[2]=="NA":
            continue
        else:
            if contri_list[2] in D2_contr:
                if contri_lv2 in D2_contr[contri_list[2]]:
                    D2_contr[contri_list[2]][contri_lv2].append(isplit[0])
                else:
                    D2_contr[contri_list[2]][contri_lv2]=[isplit[0]]
                
            else:
                D2_contr[contri_list[2]]={}
                D2_contr[contri_list[2]][contri_lv2]=[isplit[0]]
        
        contri_lv3 = ";".join(contri_list[0:3])
        if contri_list[3]=="NA":
            continue
        else:
            if contri_list[3] in D3_contr:
                if contri_lv3 in D3_contr[contri_list[3]]:
                    D3_contr[contri_list[3]][contri_lv3].append(isplit[0])
                else:
                    D3_contr[contri_list[3]][contri_lv3]=[isplit[0]]
                
            else:
                D3_contr[contri_list[3]]={}
                D3_contr[contri_list[3]][contri_lv3]=[isplit[0]]
        
        contri_lv4 = ";".join(contri_list[0:4])
        if contri_list[4]=="NA":
            continue
        else:
            if contri_list[4] in D4_contr:
                if contri_lv4 in D4_contr[contri_list[4]]:
                    D4_contr[contri_list[4]][contri_lv4].append(isplit[0])
                else:
                    D4_contr[contri_list[4]][contri_lv4]=[isplit[0]]
                
            else:
                D4_contr[contri_list[4]]={}
                D4_contr[contri_list[4]][contri_lv4]=[isplit[0]]
        
        contri_lv5 = ";".join(contri_list[0:5])
        if contri_list[5]=="NA_NA":
            continue
        else:
            if contri_list[5] in D5_contr:
                if contri_lv5 in D5_contr[contri_list[5]]:
                    D5_contr[contri_list[5]][contri_lv5].append(isplit[0])
                else:
                    D5_contr[contri_list[5]][contri_lv5]=[isplit[0]]
                
            else:
                D5_contr[contri_list[5]]={}
                D5_contr[contri_list[5]][contri_lv5]=[isplit[0]]
        
out_strain_tax.close()

#summary contradictions into one file
out_contr = open('%s/%s_contradict_sum.txt' % (sys.argv[2],sys.argv[1]), 'w')
print ("[[D1]]", file = out_contr)
for i_keys in D1_contr:
    if len(D1_contr[i_keys]) >1:
        print (i_keys+":"+"\t".join(D1_contr[i_keys].keys()), file = out_contr)

print ("[[D2]]", file = out_contr)
for i_keys in D2_contr:
    if len(D2_contr[i_keys]) >1:
        print (i_keys+":"+"\t".join(D2_contr[i_keys].keys()), file = out_contr)

print ("[[D3]]", file = out_contr)
for i_keys in D3_contr:
    if len(D3_contr[i_keys]) >1:
        print (i_keys+":"+"\t".join(D3_contr[i_keys].keys()), file = out_contr)

print ("[[D4]]", file = out_contr)
for i_keys in D4_contr:
    if len(D4_contr[i_keys]) >1:
        print (i_keys+":"+"\t".join(D4_contr[i_keys].keys()), file = out_contr)

print ("[[D5]]", file = out_contr)
for i_keys in D5_contr:
    if len(D5_contr[i_keys]) >1:
        print (i_keys+":"+"\t".join(D5_contr[i_keys].keys()), file = out_contr)

out_contr.close()



#writ the dictionaries into json files
#species dicts
js = json.dumps(D0_sp)
file = open('%s/D0_species_dic.json' % (sys.argv[2]), 'w')
file.write(js)
file.close()

js = json.dumps(D1_sp)
file = open('%s/D1_species_dic.json' % (sys.argv[2]), 'w')
file.write(js)
file.close()

js = json.dumps(D2_sp)
file = open('%s/D2_species_dic.json' % (sys.argv[2]), 'w')
file.write(js)
file.close()

js = json.dumps(D3_sp)
file = open('%s/D3_species_dic.json' % (sys.argv[2]), 'w')
file.write(js)
file.close()

js = json.dumps(D4_sp)
file = open('%s/D4_species_dic.json' % (sys.argv[2]), 'w')
file.write(js)
file.close()

js = json.dumps(D5_sp)
file = open('%s/D5_species_dic.json' % (sys.argv[2]), 'w')
file.write(js)
file.close()

js = json.dumps(D6_sp)
file = open('%s/D6_species_dic.json' % (sys.argv[2]), 'w')
file.write(js)
file.close()

#strain dic
js = json.dumps(D0_str)
file = open('%s/D0_strain_dic.json' % (sys.argv[2]), 'w')
file.write(js)
file.close()

js = json.dumps(D1_str)
file = open('%s/D1_strain_dic.json' % (sys.argv[2]), 'w')
file.write(js)
file.close()

js = json.dumps(D2_str)
file = open('%s/D2_strain_dic.json' % (sys.argv[2]), 'w')
file.write(js)
file.close()

js = json.dumps(D3_str)
file = open('%s/D3_strain_dic.json' % (sys.argv[2]), 'w')
file.write(js)
file.close()

js = json.dumps(D4_str)
file = open('%s/D4_strain_dic.json' % (sys.argv[2]), 'w')
file.write(js)
file.close()

js = json.dumps(D5_str)
file = open('%s/D5_strain_dic.json' % (sys.argv[2]), 'w')
file.write(js)
file.close()


#contradiction dic
js = json.dumps(D1_contr)
file = open('%s/D1_contradictions_dic.json' % (sys.argv[2]), 'w')
file.write(js)
file.close()

js = json.dumps(D2_contr)
file = open('%s/D2_contradictions_dic.json' % (sys.argv[2]), 'w')
file.write(js)
file.close()

js = json.dumps(D3_contr)
file = open('%s/D3_contradictions_dic.json' % (sys.argv[2]), 'w')
file.write(js)
file.close()

js = json.dumps(D4_contr)
file = open('%s/D4_contradictions_dic.json' % (sys.argv[2]), 'w')
file.write(js)
file.close()

js = json.dumps(D5_contr)
file = open('%s/D5_contradictions_dic.json' % (sys.argv[2]), 'w')
file.write(js)
file.close()









