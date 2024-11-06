data <- matrix(c(5435, 15257, 4945, 3099, 7897, 6243), nrow = 2)
print(data)
result<-fisher.test(data,workspace=2e8)
print(result)$p.value
print(log10(result$p.value))