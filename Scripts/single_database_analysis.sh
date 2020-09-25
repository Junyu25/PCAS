#!/bin/bash

#   Copyright {2015} Yuxiang Tan
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

#This script will run database analysis automatically and generate input files for primer coverage analysis.

#This script starts from the fa(can be initial or splited, this does not matter) and tax file of a database(merged or the original)
#Library file requirement:
#QIIME2 must be installed by anaconda
#NOTE1: all the input fa files must be checked about ATCG of AUCG
#NOTE2: QIIME2 or environment with vsearch must be activated

if [ $# -ne 4 ]
then
  echo ""
    echo "Usage: single_database_analysis.sh database_fa database_tax script_folder output_header"
    echo "Example:sh /home/yxtan/PCAS/scripts/single_database_analysis.sh SILVA_138_SSURef_tax_silva.fasta.fa SILVA_138_SSURef_tax_silva.fasta.tax /home/yxtan/PCAS/scripts/ SILVA_138_SSURef_tax_silva"
    echo ""
    echo "input_fa - The path to the database unaligned fa file, all Us must be convered to Ts already."
    echo "input_tax - The path to the database taxa file." 
    echo "script_folder - the folder of PCAS scripts." 
    echo "output_header - The common name header of the output files."
    exit 1
fi

#
#name the parameters
in_fa=$1
in_tax=$2
script_folder=$3
Out_head=${4}

#Check folders
if [ ! -d $script_folder ] 
then
  echo ""
  echo "Warning: The directory $script_folder does not exist in single_database_analysis.sh, exit."
  echo ""
  exit 1
fi


#check files
if [ ! -s $in_fa ] 
then
  echo ""
  echo "Warning: The file $in_fa does not exist in single_database_analysis.sh, exit."
  echo ""
  exit 1
fi

if [ ! -s $in_tax ] 
then
  echo ""
  echo "Warning: The file $in_tax does not exist in single_database_analysis.sh, exit."
  echo ""
  exit 1
fi


#the input should be fa(can be initial or splited, this does not matter) and tax
###########################################################
echo "Step 1 remove redundant sequences"
echo `date`
###########################################################
#find duplicated sequences (use the fa with/without tax name on it)
vsearch --derep_fulllength $in_fa --output $Out_head"_uniq.fna" --uc $Out_head"_uniq.uc" --threads 10
#group into groups
gist_f=$script_folder"/gist-github-qiime/"
python $gist_f"parse_otu_mapping_from_uc.py" $Out_head"_uniq.uc" $Out_head"_uniq_grouped.txt"


###########################################################
echo "Step 3 get tax for uniq sequences"
echo `date`
###########################################################
echo "Step 3.1 extract IDs from the non-redundant fa file"
cut -f2 $Out_head"_uniq_grouped.txt" > $Out_head"_grouped_ID.txt"
#the following step is not necessary anymore
#cut -f1,2 $Out_head"_uniq_grouped.txt" > $Out_head"_grouped_full_ID.txt"

echo "Step 3.2 extract taxas of non-redundant fa from the tax file"
Rscript $script_folder"/intersect_uniq_taxaID.R" file.list1=$Out_head"_grouped_ID.txt" file.list2=$in_tax file.out=$Out_head"_uniq.tax"


###########################################################
echo "Step 3.3 add consecutive str_ID add the end of the taxas seperated by ::, to make the seq and taxaID as 1:1."
echo "Step 4 generate statistic files for primer coverage calculation"
echo `date`
###########################################################
python $script_folder"/uniq_strain_tax_2_jsons.py" $Out_head"_uniq.tax" $Out_head

