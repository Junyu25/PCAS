parse_otu_mapping_from_uc.py 
Parses data from .uc files (tested with vsearch, should work with uclust/usearch too) to create an QIIME 1.X OTU mapping file. 

truncate_fasta_labels.py 
Truncates labels in a fasta file to remove everything after the initial whitespace. Usage: python truncate_fasta_labels.py X Y where X is the input fasta file and Y is the output fasta filepath. 

parse_nonstandard_chars.py 
Usage: python parse_nonstandard_chars.py X > Y where X is the input file to be parsed, and Y is the output parsed file 

parse_to_7_taxa_levels.py 
# Usage: python parse_to_7_taxa_levels.py X Y # where X is the input taxonomy mapping file, Y is the output taxonomy mapping file # Purpose is to parse output of Mike Robeson's script to force taxa into # 7 levels. 

find_all_gap_positions.py 
This file is used to generate a file (similar to the Greengenes lanemask) with 0s and 1s, representing positions that are all gaps (0) or contain non-gap (. or -) characters (1) for a given input aligned fasta file. 

split_sequences_by_domain.py 
Usage string given in beginning of file. Used to split fasta reference files by domain. Requires 

parse_taxonomy_for_clustered_subset.py 
See text at beginning of script for usage. 

insert_full_labels_into_tree.py 
Usage text is listed at beginning of file. Used to replace labels in a newick tree. 

create_majority_taxonomy.py 
See help text below about usage. Script was created to create 90% majority taxonomy strings for all sequence taxa strings in the Silva 119 release. 

create_consensus_taxonomy.py 
See help text below about usage. Script was created to create consensus taxonomy strings for all sequence taxa strings in the Silva 119 release. 

split_taxonomy_by_domain.py 
See usage string at beginning of script text. 