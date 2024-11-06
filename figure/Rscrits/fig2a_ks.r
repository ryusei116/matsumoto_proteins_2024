gene_sample1 <- read.table("1gene_sample.txt", header = FALSE)$V1
gene_sample2 <- read.table("2genes_sample.txt", header = FALSE)$V1
gene_sample3 <- read.table("3genes_sample.txt", header = FALSE)$V1
gene_sample4 <- read.table("4genes_sample.txt", header = FALSE)$V1
gene_sample5 <- read.table("5genes_sample.txt", header = FALSE)$V1


ks_test_result <- ks.test(gene_sample1, gene_sample2)
print(ks_test_result)$p.value

ks_test_result <- ks.test(gene_sample2, gene_sample3)
print(ks_test_result)$p.value

ks_test_result <- ks.test(gene_sample3, gene_sample4)
print(ks_test_result)$p.value

ks_test_result <- ks.test(gene_sample4, gene_sample5)
print(ks_test_result)$p.value