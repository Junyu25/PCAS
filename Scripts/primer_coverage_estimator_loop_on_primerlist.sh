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

#This script will run the primer coverage estimator based on a list of primers in a for loop 
#a primer file for each primer will be generated

#This script starts from unaligned fa, theoretically, dereplicated or not will not matter, but is recommanded.
#Library file requirement:Primer_prospector
#NOTE1:  Primer_prospector must be activated

if [ $# -ne 7 ]
then
  echo ""
    echo "Usage: primer_coverage_estimator_loop_on_primerlist.sh input_unaligned_fasta primer_list script_folder input_strain_tax fa_f_sub database_summary_folder output_folder"
    echo "Example:sh /home/yxtan/PCAS/scripts/primer_coverage_estimator_loop_on_primerlist.sh /home/yxtan/PCAS/other_databases/SILVA/SILVA_138/SILVA_138_SSURef_tax_silva_uniq.fna Probebase-201811-key-probes.txt /home/yxtan/PCAS/scripts/ /home/yxtan/PCAS/other_databases/SILVA/SILVA_138/SILVA_138_SSURef_tax_silva_uniq_strain.tax SILVA_138_SSURef_tax_silva_uniq /home/yxtan/PCAS/other_databases/SILVA_138_SSURef_tax_silva /home/yxtan/PCAS/primer_cov_sum" 
    echo ""
    echo "input_unaligned_fasta - The unaligned fa, all Us must be convered to Ts already, and should be dereplicated already."
    echo "primer_list - The primer-list info from probase."
    echo "script_folder - the folder of scripts."
    echo "input_strain_tax - the uniq strain tax file of the input_unaligned_fasta."
    echo "fa_f_sub - the sub-str of fa file name：(such as SILVA_138_SSURef_tax_silva_uniq)"
    echo "database_summary_folder - the folder of dictionary json files of the database (such as /home/yxtan/PCAS/other_databases/SILVA_138_SSURef_tax_silva)."
    echo "output_folder - the folder path of the primer analysis summaries should go, (such as /home/yxtan/PCAS/primer_cov_sum)"
    exit 1
fi

#name the parameters
fa_f=$1
primer_list=$2
script_folder=$3
tax_f=$4
fa_f_sub=$5
database_summary_folder=$6
output_folder=$7

#check files
if [ ! -s $fa_f ] 
then
  echo ""
  echo "Warning: The file $fa_f does not exist in primer_coverage_estimator_loop_on_primerlist.sh, exit."
  echo ""
  exit 1
fi

if [ ! -s $tax_f ] 
then
  echo ""
  echo "Warning: The file $tax_f does not exist in primer_coverage_estimator_loop_on_primerlist.sh, exit."
  echo ""
  exit 1
fi

if [ ! -s $primer_list ] 
then
  echo ""
  echo "Warning: The file $primer_list does not exist in primer_coverage_estimator_loop_on_primerlist.sh, exit."
  echo ""
  exit 1
fi

#Check folders
if [ ! -d $script_folder ] 
then
  echo ""
  echo "Warning: The directory $script_folder does not exist in primer_coverage_estimator_loop_on_primerlist.sh, exit."
  echo ""
  exit 1
fi

if [ ! -d $database_summary_folder ] 
then
  echo ""
  echo "Warning: The directory $database_summary_folder does not exist in primer_coverage_estimator.sh, exit."
  echo ""
  exit 1
fi

#Check folders
if [ ! -d $output_folder ] 
then
  echo ""
  echo "Warning: The directory $output_folder does not exist in primer_coverage_estimator.sh, generate it."
  echo ""
  mkdir $output_folder
fi

################
echo "step 1, get only the shortname and the seq from the primer_list file."
echo `date`
###############
cut -f1 $primer_list | sort -u > $primer_list"_ID.txt"
cut -f1,4 $primer_list | sort -u > $primer_list"_ID_seq.txt"

for i in $(cat $primer_list"_ID.txt")
do 
    #for samtools, the region file must be the chr:from-to format or only the chr, as a result, here, only the readname without > is used. 
    grep $i $primer_list"_ID_seq.txt" > "Primers_"$i".txt"

    if [ ! -s "Primers_"$i".txt" ] 
    then
      echo ""
      echo "Warning: The file Primers_ $i .txt did not generated in primer_coverage_estimator_loop_on_primerlist.sh, exit."
      echo ""
      exit 1
    fi
   
    ################
    echo "step 2, run primer_coverage_estimator.sh on the Primers_ $i .txt."
    echo `date`
    ###############
    sh $script_folder"/primer_coverage_estimator.sh" $fa_f "Primers_"$i".txt" $i $script_folder $tax_f $fa_f_sub $database_summary_folder $output_folder
done

