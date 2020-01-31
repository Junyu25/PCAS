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


#this script is to use the faID to get taxa
#example: Rscript $script_folder"/extract_taxa_by_ID.R" file.list1="515Yf/515Yf_ID.txt" file.list2="/home/yxtan/PCAS/other_databases/SILVA/SILVA_138/SILVA_138_SSURef_tax_silva_uniq_strain.tax"

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
	stop("\n\nWarning: Usage: file.list1( _ID.txt) is not exist, please check the path. \n\n")
}

#check whether file in is exist
if (!exists("file.list2")) {
	stop("\n\nWarning: Usage: file.list2(_uniq_strain.tax) is not exist, please check the path. \n\n")
}


#read two list of ID
list1<-read.delim2(file=file.list1,header=FALSE,stringsAsFactors=FALSE)
list2<-read.delim2(file=file.list2,header=FALSE,stringsAsFactors=FALSE,sep = " ")


#merge by the first column (fa ID)
m1 <- merge(list1, list2, by.x = "V1", by.y = "V1")

#output the file
write.table(m1, file=paste(file.list1,"_merge_taxa.txt",sep = ""),  row.names = FALSE , col.names = FALSE, quote=FALSE)