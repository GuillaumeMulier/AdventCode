# Day 5 advent of code 2024 #

# Part 1 ----

Chemin <- "C:/Users/gmulier/Documents/Github/AdventCode/2024"
Input <- readLines(paste0(Chemin, "/Input/day5.txt"))
Separation <- which(Input == "")
Ordering <- Input[seq(1, Separation - 1)]
Updates <- strsplit(Input[seq(Separation + 1, length(Input))], ",")

DfRegles <- as.data.frame(do.call("rbind", strsplit(Ordering, "\\|")))
ListeRegles <- tapply(DfRegles$V1, DfRegles$V2, c)

VerifOrdre <- function(Vec) {
  WrgOrder <- vapply(seq_along(Vec)[-length(Vec)], \(index) {
    NbCours <- Vec[index]
    Suite <- Vec[seq(index + 1, length(Vec))]
    if (NbCours %in% names(ListeRegles)) {
      return(any(Suite %in% ListeRegles[[NbCours]]))
    } else {
      return(FALSE)
    }
  }, logical(1))
  return(any(WrgOrder))
}
Nbs <- vapply(Updates, \(x) {
  if (VerifOrdre(x)) {
    return(0)
  } else {
    return(as.numeric(x[length(x) %/% 2 + 1]))
  }
}, numeric(1))
print(paste0("Réponse partie 1 : ", sum(Nbs)))


# Part 2 ----

Incorrects <- Updates[Nbs == 0]
ReorderVec <- function(Vec) {
  StackNb <- Vec
  VecOrdered <- Vec
  while(length(StackNb) > 0) {
    Positions <- vapply(StackNb, \(x) which(x == VecOrdered), numeric(1))
    Element <- VecOrdered[Positions[Positions == min(Positions)]]
    Suite <- VecOrdered[seq(which(Element == VecOrdered), length(VecOrdered))]
    AReplacer <- Suite[Suite %in% ListeRegles[[Element]]]
    if (length(AReplacer)) VecOrdered <- c(AReplacer, VecOrdered[!VecOrdered %in% AReplacer])
    StackNb <- StackNb[StackNb != Element]
  }
  return(as.numeric(VecOrdered[length(VecOrdered) %/% 2 + 1]))
}
print(paste0("Réponse partie 2 : ", sum(vapply(Incorrects, ReorderVec, numeric(1)))))

