#!/usr/bin/python
from __future__ import print_function
import re,sys,os

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

#This script will read in column of primer IDs (following rules of DPSN:the first and last two char are not number and the 5' loc in the middle) and separate them into forward and reverse dict and generate pair. 

#This script starts from list of IDs (such as DPSN_final_V6_SSU_ID.txt)
#The output will be its _pair.txt (DPSN_final_V6_SSU_ID.txt_pair.txt)
#Library file requirement: python 2.7 and up

#Usage: python generate_primer_pair_form_IDlist.py ID_list


in_ID_list=sys.argv[1]
#########check files and folders  
if not os.path.isfile(in_ID_list):
    print('Input ID_list file is not exist; Exit now.')
    exit(0)


#build dic
forw_dic={}
rev_dic={}


#read the file into two dictionary
with open(in_ID_list) as infile:
    for i in infile:
        isplit = i.rstrip()
        #extract the location number by the DPSN rule: the first and last two char are not number and the 5' loc in the middle)
        loc_num = isplit[2:-2]
        str_id = isplit[-1]
        if str_id == "f":
            if loc_num in forw_dic:
                forw_dic[loc_num].append(isplit)
            else:
                forw_dic[loc_num]=[isplit]
        elif str_id == "r":
            if loc_num in rev_dic:
                rev_dic[loc_num].append(isplit)
            else:
                rev_dic[loc_num]=[isplit]
        else:
            print('Warning: the primer %s is not following rule, ignore it now.')


#compare two dic and generate pair list.
out_pair = open('%s_pair.txt' % (in_ID_list), 'w')
for f_keys in forw_dic:
    for r_keys in rev_dic:
        if int(f_keys) < int(r_keys):
            f_value = forw_dic[f_keys]
            r_value = rev_dic[r_keys]
            for f_v in f_value:
                for r_v in r_value:
                    print (f_v+"+"+r_v, file = out_pair)

out_pair.close()










