#Take in output .dot file from dep viz and find leaf nodes

#install.packages("data.table")
#install.packages("stringr")
library(data.table)
library(stringr)

#parse DOT file
dotraw <- fread("/stuff/modularity-dep-viz/example1.dot",skip=2,header=FALSE)
dotraw[, V3 := str_replace_all(V2,";","") ]
dotraw[, V4 := str_replace_all(V3,'"','') ]
dotraw[, V5 := strsplit(V4,split=" -> ", fixed=TRUE) ]
dotraw2 <- dotraw[lapply(dotraw$V5,length)==2,]
dotraw3 <- dotraw2[!duplicated(V5)]
dotfix <- data.table(sapply(dotraw3$V5,function(x) x[1]),sapply(dotraw3$V5,function(x) x[2]))
colnames(dotfix) <- c("origin","deps")

#find leaf nodes
setdiff(dotfix$origin,dotfix$deps)

#find ez to include in modules RPMs, not very graceful
#all the deps that have only 1 origin
dotfix$deps[which(!(dotfix$deps %in% dotfix$deps[duplicated(dotfix$deps)]))]
#all the deps that have origins exclusively of those in above list





#could set up in graph database




#str_split_fixed(before$type, "_and_", 2)






#dotraw2 <- dotraw[length(V4[[1]])!=1] 



#dotraw[,V1:=NULL]

#dotraw[, origin := str_replace(str_replace(str_replace(strsplit(V2,split=" -> ", fixed=TRUE),"\\\\",""),"'",""),";","") ]
#dotraw[, origin2 := origin[1] ]

#dotraw[, dep := str_replace(str_replace(str_replace(strsplit(V2,split=" -> ", fixed=TRUE),"\\\\",""),"'",""),";","")[[2]] ]
#dotraw[,V2:=NULL]



#str_replace_all(str1, "([\n\t])", "")



#strsplit("\"apr-util\" -> \"BASE-RUNTIME\";",split=" -> ", fixed=TRUE)
