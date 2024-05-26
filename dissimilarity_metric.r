library("ape")
library("Quartet")
library("TreeDist")

glottolog_tree <- ape::read.tree("trees/reference_tree.nwk")
trees <- read.csv("trees/newicks.tsv", sep = "\t")
for (i in 1:nrow(trees)) {
  tree <- ape::read.tree(text = trees$Newick[i])
  trees$SteelPenny[i] <- SteelPenny(QuartetStatus(glottolog_tree, tree), similarity = FALSE)
  trees$RobinsonFoulds[i] <- InfoRobinsonFoulds(glottolog_tree, tree)
}
newick_index <- which(colnames(trees) == "Newick")
trees <- trees[, -newick_index]
write.csv(trees, "trees/dissimilarity_metrics.csv", row.names = FALSE, quote = FALSE)
