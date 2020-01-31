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

#This script will run the in silico primer-pair matching and statistics automatically in a for loop on primer pairs

#This script starts from unaligned fa, theoretically, dereplicated or not will not matter, but is recommanded.
#Library file requirement:Primer_prospector
#NOTE1:  Primer_prospector must be activated
#recommended workding directory is the primer_coverage folder

if [ $# -ne 7 ]
then
  echo ""
    echo "Usage: primer_pair_coverage_estimator_loop_on_primerlist_pair.sh input_unaligned_fasta primer_pair_list script_folder input_strain_tax fa_f_sub database_summary_folder output_folder"
    echo "Example:sh /home/yxtan/PCAS/scripts/primer_pair_coverage_estimator_loop_on_primerlist_pair.sh /home/yxtan/PCAS/other_databases/SILVA/SILVA_138/SILVA_138_SSURef_tax_silva_uniq.fna Probebase-201811-key-probes_pair.txt /home/yxtan/PCAS/scripts/ /home/yxtan/PCAS/other_databases/SILVA/SILVA_138/SILVA_138_SSURef_tax_silva_uniq_strain.tax SILVA_138_SSURef_tax_silva_uniq /home/yxtan/PCAS/other_databases/SILVA_138_SSURef_tax_silva /home/yxtan/PCAS/primer_cov_sum"
    echo ""
    echo "input_unaligned_fasta - The unaligned fa, all Us must be convered to Ts already."
    echo "primer_list - The primer-list of pair of ID forward+reward"
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
fa_f_sub=${5}
database_summary_folder=$6
output_folder=$7

#check files
if [ ! -s $fa_f ] 
then
  echo ""
  echo "Warning: The file $fa_f does not exist in primer_pair_coverage_estimator_loop_on_primerlist_pair.sh, exit."
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
  echo "Warning: The directory $script_folder does not exist in primer_pair_coverage_estimator_loop_on_primerlist_pair.sh, exit."
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

if [ ! -d $output_folder ] 
then
  echo ""
  echo "Warning: The directory $output_folder does not exist in primer_coverage_estimator.sh, generate it."
  echo ""
  mkdir $output_folder
fi

################
echo "step 0, get the primer_f_name and primer_r_name row by row."
echo `date`
###############
for i in $(cat $primer_list)
do 
    #the pair is connected by a +
    OLD_IFS="$IFS" 
    IFS="+" 
    arr=($i) 
    IFS="$OLD_IFS" 
    primer_f_name=${arr[0]} 
    primer_r_name=${arr[1]}
    echo $primer_f_name
    echo $primer_r_name
    
    if [ ! -s $primer_f_name"_"$fa_f_sub"_hits.txt" ] 
    then
      echo ""
      echo "Warning: The file $primer_f_name _ $fa_f_sub _hits.txt does not exist in primer_pair_coverage_estimator_loop_on_primerlist_pair.sh, exit."
      echo ""
      exit 1
    fi
    
    if [ ! -s $primer_r_name"_"$fa_f_sub"_hits.txt" ] 
    then
      echo ""
      echo "Warning: The file $primer_r_name _ $fa_f_sub _hits.txt does not exist in primer_pair_coverage_estimator_loop_on_primerlist_pair.sh, exit."
      echo ""
      exit 1
    fi
    
    #run primer_pair_coverage_estimator.sh
    sh $script_folder"/primer_pair_coverage_estimator.sh" $fa_f $primer_f_name $primer_r_name $script_folder $tax_f $fa_f_sub $database_summary_folder $output_folder
    
 done
