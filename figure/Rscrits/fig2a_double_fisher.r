data <- matrix(c(5435, 8514, 4945, 1957, 7897, 3971), nrow = 2)
print(data)
result <- fisher.test(data,workspace=2e8)
print(result)$p.value
