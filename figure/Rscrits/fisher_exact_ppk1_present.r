data <- matrix(c(4545,4336,6938,  
                 890,609,959), 
               nrow = 2,byrow = TRUE)
rownames(data) <- c("PPK1 Present", "PPK1 Absent")
colnames(data) <- c("c1","c2","c3")
print(data)

result = fisher.test(data,workspace=2e8)
print(result)$p.value