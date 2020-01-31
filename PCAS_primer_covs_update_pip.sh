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

#This pipeline will run database analysis automatically and then primer coverage analysis
#The output is current folder, and the key output for the database will be in the inputted output_folder path
#It is recommended to put the primer list in a separated folder in order (such as primer_seqs) to minimize the files in the current folder 

#This script starts from the fa(can be initial or splited, this does not matter) and tax file of a database(merged or the original)
#Library file requirement:
#QIIME2 must be installed by anaconda
#NOTE1: all the input fa files must be checked about ATCG of AUCG
#NOTE2: QIIME2 or environment with vsearch must be activated
#NOTE3:  Primer_prospector must be activated

if [ $# -ne 7 ]
then
  echo ""
    echo "Usage: PCAS_primer_covs_update_pip.sh database_fa database_tax primer_list primer_pair_list script_folder output_header output_folder"
    echo "Example:sh /home/yxtan/PCAS/scripts/PCAS_primer_covs_update_pip.sh SILVA_138_SSURef_tax_silva.fasta.fa SILVA_138_SSURef_tax_silva.fasta.tax /home/yxtan/PCAS/DPSN_primers/DPSN_final_V6_SSU_ID.txt /home/yxtan/PCAS//DPSN_primers/DPSN_final_V6_SSU_ID.txt_pair.txt /home/yxtan/PCAS/scripts/ SILVA_138_SSURef_tax_silva PCAS_primer_file_out"
    echo ""
    echo "input_unaligned_fasta - The path to the database unaligned fa file, all Us must be convered to Ts already"
    echo "input_tax - The path to the database taxa file." 
    echo "primer_list - The primer-list info with ID and Seq in the 1st and 4th columns."
    echo "primer_list_pair - The list of pairs of primers (such as primerF+primerR) ."
    echo "script_folder - the folder of PCAS scripts." 
    echo "output_header - The common name header of the output files."
    echo "output_folder - the folder path of the primer analysis summaries should go, (such as /home/yxtan/PCAS/primer_cov_sum)"
       
    exit 1
fi

#name the parameters
in_fa=$1
in_tax=$2
primer_list=$3
primer_pair_list=$4
script_folder=$5
Out_head=${6}
output_folder=$7

#check files
if [ ! -s $in_fa ] 
then
  echo ""
  echo "Warning: The file $in_fa does not exist in PCAS_primer_covs_update_pip.sh, exit."
  echo ""
  exit 1
fi

if [ ! -s $in_tax ] 
then
  echo ""
  echo "Warning: The file $in_tax does not exist in PCAS_primer_covs_update_pip.sh, exit."
  echo ""
  exit 1
fi

if [ ! -s $primer_list ] 
then
  echo ""
  echo "Warning: The file $primer_list does not exist in PCAS_primer_covs_update_pip.sh, exit."
  echo ""
  exit 1
fi

if [ ! -s $primer_pair_list ] 
then
  echo ""
  echo "Warning: The file $primer_pair_list does not exist in PCAS_primer_covs_update_pip.sh, exit."
  echo ""
  exit 1
fi

#Check folders
if [ ! -d $script_folder ] 
then
  echo ""
  echo "Warning: The directory $script_folder does not exist in PCAS_primer_covs_update_pip.sh, exit."
  echo ""
  exit 1
fi

if [ ! -d $output_folder ] 
then
  echo ""
  echo "Warning: The directory $output_folder does not exist in PCAS_primer_covs_update_pip.sh, generate it."
  echo ""
  mkdir $output_folder
fi


################
echo "step 1, analyze the database first."
echo `date`
###############
sh $script_folder"/single_database_analysis.sh" $in_fa $in_tax $script_folder $Out_head

derep_fa=$Out_head"_uniq.fna"
input_strain_tax=$Out_head"_uniq_strain.tax"
database_summary_folder=$Out_head
fa_f_sub=$Out_head"_uniq"
################
echo "step 2, run on single primers."
echo `date`
###############
sh $script_folder"/primer_coverage_estimator_loop_on_primerlist.sh" $derep_fa $primer_list $script_folder $input_strain_tax $fa_f_sub $database_summary_folder $output_folder


################
echo "step 3, run on the primer pairs based on the single primers."
echo `date`
###############
sh $script_folder"/primer_pair_coverage_estimator_loop_on_primerlist_pair.sh" $derep_fa $primer_pair_list $script_folder $input_strain_tax $fa_f_sub $database_summary_folder $output_folder


