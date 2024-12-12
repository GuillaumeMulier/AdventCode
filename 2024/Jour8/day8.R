# Day 8 advent of code 2024 #

# Part 1 ----

Chemin <- "C:/Users/gmulier/Documents/Github/AdventCode/2024"
Input <- readLines(paste0(Chemin, "/Input/day8.txt"))
Input <- matrix(unlist(strsplit(Input, "")), length(Input), nchar(Input[[1]]), byrow = TRUE)

ListeAntennes <- lapply(unique(Input[Input != "."]), \(x) which(Input == x, arr.ind = TRUE))
names(ListeAntennes) <- unique(Input[Input != "."])
CreateAnti <- function(R1, R2, C1, C2) {
  PenteX <- C2 - C1
  PenteY <- R2 - R1
  return(matrix(c(R2 + PenteY, R1 - PenteY, C2 + PenteX, C1 - PenteX), 2, 2))
}
AntiNodes <- do.call("rbind", lapply(ListeAntennes, \(Tab) {
  MatAnti <- matrix(nrow = 0, ncol = 2)
  for(i in seq(1, nrow(Tab) - 1)) {
    for (j in seq(i + 1, nrow(Tab))) {
      MatAnti <- rbind(MatAnti, CreateAnti(Tab[i, 1], Tab[j, 1], Tab[i, 2], Tab[j, 2]))
    }
  }
  return(MatAnti)
}))
AntiNodes <- AntiNodes[AntiNodes[, 1] > 0 & AntiNodes[, 2] > 0 & AntiNodes[, 1] <= nrow(Input) & AntiNodes[, 2] <= ncol(Input), ]
AntiNodes <- AntiNodes[!duplicated(paste0(AntiNodes[, 1], "-", AntiNodes[, 2])), ]
print(paste0("Réponse partie 1 : ", nrow(AntiNodes)))


# Part 2 ----

CreateAntiUnconstr <- function(R1, R2, C1, C2, NRows, NCols) {
  PenteX <- C2 - C1
  PenteY <- R2 - R1
  # Could be optimized to restrict the number of points searched
  NbPtsMax <- min(ceiling(abs(NCols / PenteX)), ceiling(abs(NRows / PenteY)))
  return(matrix(c(R2 + PenteY * seq(1, NbPtsMax), R1 - PenteY * seq(1, NbPtsMax), C2 + PenteX * seq(1, NbPtsMax), C1 - PenteX * seq(1, NbPtsMax)), ncol = 2))
}
AntiNodes <- do.call("rbind", lapply(ListeAntennes, \(Tab) {
  MatAnti <- matrix(nrow = 0, ncol = 2)
  for(i in seq(1, nrow(Tab) - 1)) {
    for (j in seq(i + 1, nrow(Tab))) {
      MatAnti <- rbind(MatAnti, CreateAntiUnconstr(Tab[i, 1], Tab[j, 1], Tab[i, 2], Tab[j, 2], nrow(Input), ncol(Input)))
    }
  }
  return(MatAnti)
}))
AntiNodes <- AntiNodes[AntiNodes[, 1] > 0 & AntiNodes[, 2] > 0 & AntiNodes[, 1] <= nrow(Input) & AntiNodes[, 2] <= ncol(Input), ]
AntiNodes <- AntiNodes[!duplicated(paste0(AntiNodes[, 1], "-", AntiNodes[, 2])), ]
Input[AntiNodes] <- "#"
print(paste0("Réponse partie 2 : ", sum(Input != ".")))
