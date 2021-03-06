##Generally use this R version: /share/apps/R/R-2.12.2_gnu412_x86_64_vanilla/bin/Rscript --vanilla 

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


#this script is to calculate the percentage of primer vs database background
#Rscript $script_folder"/coverage_calculate.R" file.list1="515Yf/D0_stat_all.txt" file.list2="/thinker/net/biosoft/16S_ref_databases/SILVA132_EZ18_GG138/intermediate/D0/D0_stat_all.txt"

#check arguments
for (e in commandArgs()) {
        ta = strsplit(e,"=",fixed=TRUE)
        if(! is.na(ta[[1]][2])) {
                temp = ta[[1]][2]
                if(substr(ta[[1]][1],nchar(ta[[1]][1]),nchar(ta[[1]][1])) == "I") {
                temp = as.integer(temp)
                }
        if(substr(ta[[1]][1],nchar(ta[[1]][1]),nchar(ta[[1]][1])) == "N") {
                temp = as.numeric(temp)
                }
        assign(ta[[1]][1],temp)
        } else {
        assign(ta[[1]][1],TRUE)
        }
}

#check whether file in is exist
if (!exists("file.list1")) {
	stop("\n\nWarning: Usage: file.list1( _stat_all.txt of primer) is not exist, please check the path. \n\n")
}

#check whether file in is exist
if (!exists("file.list2")) {
	stop("\n\nWarning: Usage: file.list2(_stat_all.txt of the full database) is not exist, please check the path. \n\n")
}

#read two list of ID
list1<-read.delim2(file=file.list1,header=FALSE,stringsAsFactors=FALSE,row.names=1)
list2<-read.delim2(file=file.list2,header=FALSE,stringsAsFactors=FALSE,row.names=1)

list_out<-list1/list2
m1 <- merge(list1, list2, by="row.names")
m2 <- merge(m1, list_out, by.x="Row.names", by.y="row.names")


colnames(m2)<- c("taxonomy","species_num_primer","seq_num_primer","species_num_bg","seq_num_bg","taxa-species","unique-sequence")



#output the file
write.table(m2, file=paste(file.list1,"_cover_percentage.txt",sep = ""),  row.names = FALSE , col.names = TRUE, quote=FALSE, sep="\t")