file_name="./test/id680307.fasta.fa"
con <- file(file_name, "r")

#generate a matrix which have 50000 col and 6 row
col_num=50000
out_matrix <- matrix(0, nrow=6,ncol=col_num)
rownames(out_matrix)=c("A","T","C","G","-",".")
colnames(out_matrix)=1:col_num

line=readLines(con,n=1)

while( length(line) != 0 ) {
  #timestart<-Sys.time()
  if (substring(line, 1, 1)!=">")
  {
    #deal with the string one time only, in order to save time (saved 200 fold time)
    str_list=strsplit(line, split="")[[1]]
    
    #check each base and add into the matrix
    for(i in 1:col_num){
        if(str_list[i]=="A")
      {
        out_matrix[1,i]=out_matrix[1,i]+1
      } else if(str_list[i]=="T")
      {
        out_matrix[2,i]=out_matrix[2,i]+1
      } else if(str_list[i]=="C")
      {
        out_matrix[3,i]=out_matrix[3,i]+1
      } else if(str_list[i]=="G")
      {
        out_matrix[4,i]=out_matrix[4,i]+1
      } else if(str_list[i]=="-")
      {
        out_matrix[5,i]=out_matrix[5,i]+1
      } else if(str_list[i]==".")
      {
        out_matrix[6,i]=out_matrix[6,i]+1
      }
    }
  }
  
  #timeend<-Sys.time()
  #runningtime<-timeend-timestart
  #print(runningtime)
  
  #go to next line
  line=readLines(con,n=1)
}

write.table(out_matrix, file=paste(file_name,"_freq_summary.txt",sep = ""),sep="\t", row.names= TRUE )

close(con)
