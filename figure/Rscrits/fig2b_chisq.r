data <- matrix(c(2223,1142,2926,186,443,301,  
                 2509.631491483174,1153.711258828417,2341.025758205235,132.59413516133498,538.1004708489129,545.9368854729263), 
               nrow = 2,byrow = TRUE)
rownames(data) <- c("Observed", "Expected")
colnames(data) <- c("c1c1","c1c2","c1c3","c2c2","c2c3","c3c3")
print(data)
result <- chisq.test(data)
print(result)$p.value
print(log10(result$p.value))