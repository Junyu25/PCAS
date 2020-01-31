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

#This script will run the in silico primer-pair matching and statistics automatically

#This script starts from unaligned fa, theoretically, dereplicated or not will not matter, but is recommanded.
#Library file requirement:Primer_prospector
#NOTE1:  Primer_prospector must be activated
#recommended workding directory is the primer_coverage folder

if [ $# -ne 8 ]
then
  echo ""
    echo "Usage: primer_pair_coverage_estimator.sh input_unaligned_fasta primer_f_name primer_r_name script_folder input_strain_tax fa_f_sub database_summary_folder output_folder"
    echo "Example:sh /home/yxtan/PCAS/scripts/primer_pair_coverage_estimator.sh /home/yxtan/PCAS/other_databases/SILVA/SILVA_138/SILVA_138_SSURef_tax_silva_uniq.fna 515Yf 907r /home/yxtan/PCAS/scripts/ /home/yxtan/PCAS/other_databases/SILVA/SILVA_138/SILVA_138_SSURef_tax_silva_uniq_strain.tax SILVA_138_SSURef_tax_silva_uniq /home/yxtan/PCAS/other_databases/SILVA_138_SSURef_tax_silva /home/yxtan/PCAS/primer_cov_sum"
    echo ""
    echo "input_unaligned_fasta - The unaligned fa, all Us must be convered to Ts already, and should be dereplicated already."
    echo "primer_f_name - The name of the forward primer."
    echo "primer_r_name - The name of the reverse primer."
    echo "script_folder - the folder of scripts: /home/yxtan/PCAS/scripts/"
    echo "input_strain_tax - the uniq strain tax file of the input_unaligned_fasta."
    echo "fa_f_sub - the sub-str of fa file name：(such as SILVA_138_SSURef_tax_silva_uniq)"
    echo "database_summary_folder - the folder of dictionary json files of the database (such as /home/yxtan/PCAS/other_databases/SILVA_138_SSURef_tax_silva)."
    echo "output_folder - the folder path of the primer analysis summaries should go, (such as /home/yxtan/PCAS/primer_cov_sum)"
    exit 1
fi

#name the parameters
fa_f=$1
primer_f_name=$2
primer_r_name=$3
script_folder=$4
tax_f=$5
fa_f_sub=${6}
database_summary_folder=$7
output_folder=$8

#check files
if [ ! -s $fa_f ] 
then
  echo ""
  echo "Warning: The file $fa_f does not exist in primer_pair_coverage_estimator.sh, exit."
  echo ""
  exit 1
fi

if [ ! -s $primer_f_name"_"$fa_f_sub"_hits.txt" ] 
then
  echo ""
  echo "Warning: The file $primer_f_name _ $fa_f_sub _hits.txt does not exist in primer_pair_coverage_estimator.sh, exit."
  echo ""
  exit 1
fi

if [ ! -s $primer_r_name"_"$fa_f_sub"_hits.txt" ] 
then
  echo ""
  echo "Warning: The file $primer_r_name _ $fa_f_sub _hits.txt does not exist in primer_pair_coverage_estimator.sh, exit."
  echo ""
  exit 1
fi

#Check folders
if [ ! -d $script_folder ] 
then
  echo ""
  echo "Warning: The directory $script_folder does not exist in primer_pair_coverage_estimator.sh, exit."
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
echo "step 1, get amplicons using primer_hits pair."
echo `date`
###############
#get the output name format
echo $primer_f_name"_"$fa_f_sub"_hits.txt:"$primer_r_name"_"$fa_f_sub"_hits.txt"

#get fa
get_amplicons_and_reads.py -f $fa_f -i $primer_f_name"_"$fa_f_sub"_hits.txt:"$primer_r_name"_"$fa_f_sub"_hits.txt" -o $primer_f_name"_"$primer_r_name -R 250
out_header=$primer_f_name"_"$primer_r_name"/"$primer_f_name"_"$primer_r_name

if [ ! -s $out_header"_amplicons.fasta" ] 
then
  echo ""
  echo "Warning: The file $out_header _amplicons.fasta was not generated in primer_pair_coverage_estimator.sh step2 failed, exit."
  echo ""
  exit 1
fi

#get amplicon length statistics
#this step is not necessary and require pandas library 
#python $script_folder"/amplicon-length-analysis.py" $out_header"_amplicons.fasta"


################
echo "step 2, do coverage statistics on primer-pair."
echo `date`
###############
#extract ID from amplicons.fasta
grep "^>" $out_header"_amplicons.fasta" > $out_header"_ID.txt"
#delete the > from the ID file
sed -i "s/>//g" $out_header"_ID.txt"
#get taxa from faID
Rscript $script_folder"/extract_taxa_by_ID.R" file.list1=$out_header"_ID.txt" file.list2=$tax_f
out_taxa=$out_header"_ID.txt_merge_taxa.txt"

#run analysis on the ID_merge_taxa file for each primer and get the summary
python $script_folder"/primer_taxa_coverage_calculator.py" $out_header"_ID.txt_merge_taxa.txt" $database_summary_folder $output_folder"/"$primer_f_name"-"$primer_r_name



 
