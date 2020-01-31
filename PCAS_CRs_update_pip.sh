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

#This pipeline will run the ATCG freq database and the conserved region searching automatically for each SILVA update
#The output is current folder

#This script starts from The full-aligned fa from SILVA, which must be unzipped.
#Library file requirement:
#NOTE1: Rscript must be activated, also the biopython in python. Generally, they can be activated in QIIME

if [ $# -ne 4 ]
then
  echo ""
    echo "Usage: PCAS_CRs_update_pip.sh input_full_aligned_fasta Ecoli_MG1655_make_order step_width script_folder"
    echo "Example:sh /home/yxtan/PCAS/scripts/PCAS_CRs_update_pip.sh ../SILVA_138_PCAS/SILVA_138_SSURef_tax_silva_full_align_trunc.fasta /home/yxtan/PCAS/scripts/Ecoli.K-12substr.MG1655.fa_mark_order.txt 7 /home/yxtan/PCAS/scripts/"
    echo ""
    echo "input_full_aligned_fasta - The full-aligned fa from SILVA, must be unzipped"
    echo "Ecoli_MG1655_make_order - The path to Ecoli_MG1655_make_order file."
    echo "step_width - step_width used for summary, default is 7."
    echo "script_folder - the folder of scripts."
       
    exit 1
fi

#name the parameters
fa_f=$1
Ecoli_f=$2
step_width=$3
script_folder=$4


#check files
if [ ! -s $fa_f ] 
then
  echo ""
  echo "Warning: The file $fa_f does not exist in PCAS_CRs_update_pip.sh, exit."
  echo ""
  exit 1
fi

if [ ! -s $Ecoli_f ] 
then
  echo ""
  echo "Warning: The file $Ecoli_f does not exist in PCAS_CRs_update_pip.sh, exit."
  echo ""
  exit 1
fi

#Check folders
if [ ! -d $script_folder ] 
then
  echo ""
  echo "Warning: The directory $script_folder does not exist in PCAS_CRs_update_pip.sh, exit."
  echo ""
  exit 1
fi

################
echo "step 1, run split and convert."
echo `date`
###############
python $script_folder"/SILVA_2_fa_tax.py" $fa_f
fa_f_base=$(basename $fa_f)
input_fa=$fa_f_base".fa"
input_tax=$fa_f_base".tax"

python $script_folder"/Split_fasta_base_on_domain.py" $fa_f
input_BAC="Bacteria.fasta"
input_ARC="Archaea.fasta"
input_EUK="Eukaryota.fasta"

python $script_folder"/SILVA_2_fa_tax.py" $input_BAC
input_BAC_fa=$input_BAC".fa"
input_BAC_tax=$input_BAC".tax"

python $script_folder"/SILVA_2_fa_tax.py" $input_ARC
input_ARC_fa=$input_ARC".fa"
input_ARC_tax=$input_ARC".tax"

python $script_folder"/SILVA_2_fa_tax.py" $input_EUK
input_EUK_fa=$input_EUK".fa"
input_EUK_tax=$input_EUK".tax"


################
echo "step 2, run CRs."
echo `date`
###############
sh $script_folder"/conserved_region_summary.sh" $input_fa $Ecoli_f $step_width $script_folder

sh $script_folder"/conserved_region_summary.sh" $input_BAC_fa $Ecoli_f $step_width $script_folder
sh $script_folder"/conserved_region_summary.sh" $input_ARC_fa $Ecoli_f $step_width $script_folder
sh $script_folder"/conserved_region_summary.sh" $input_EUK_fa $Ecoli_f $step_width $script_folder

################
echo "step 3, run stat on phylum."
echo `date`
###############
sh $script_folder"/SILVA_conserved_region_summary_loop_phylum.sh" $input_fa $Ecoli_f $step_width $script_folder $input_tax "All"

sh $script_folder"/SILVA_conserved_region_summary_loop_phylum.sh" $input_BAC_fa $Ecoli_f $step_width $script_folder $input_BAC_tax "Bacteria"
sh $script_folder"/SILVA_conserved_region_summary_loop_phylum.sh" $input_ARC_fa $Ecoli_f $step_width $script_folder $input_ARC_tax "Archaea"
sh $script_folder"/SILVA_conserved_region_summary_loop_phylum.sh" $input_EUK_fa $Ecoli_f $step_width $script_folder $input_EUK_tax "Eukaryota"

