# Day 4 advent of code 2024 #

# Part 1 ----

Chemin <- "C:/Users/gmulier/Documents/Github/AdventCode/2024"
Input <- readLines(paste0(Chemin, "/Input/day4.txt"))
NRows <- length(Input)
NCols <- nchar(Input)
WordPuzzle <- matrix(unlist(strsplit(Input, "")), NRows, NCols, byrow = TRUE)

VerifMot <- function(Vec) all(Vec[1] == "X", Vec[2] == "M", Vec[3] == "A", Vec[4] == "S")
VerifVec <- function(Vec) {
  Long <- length(Vec)
  if (Long < 4) {
    return(0)
  } else {
    # Forward
    Debuts <- seq(1, Long - 3)
    Fins <- seq(4, Long)
    Forward <- sum(vapply(seq_along(Debuts), \(index) VerifMot(Vec[seq(Debuts[index], Fins[index])]), logical(1)))
    # Backward
    Debuts <- seq(Long, 4)
    Fins <- seq(Long - 3, 1)
    Backward <- sum(vapply(seq_along(Debuts), \(index) VerifMot(Vec[seq(Debuts[index], Fins[index])]), logical(1)))
    return(Forward + Backward)
  }
}
VerifMatrice <- function(Mat) {
  NRows <- nrow(Mat)
  NCols <- ncol(Mat)
  NMatches <- 0
  # Line checking
  NMatches <- NMatches + sum(vapply(seq_len(NRows), \(l) VerifVec(Mat[l, ]), numeric(1)))
  # Column checking
  NMatches <- NMatches + sum(vapply(seq_len(NCols), \(l) VerifVec(Mat[, l]), numeric(1)))
  # Diagonal checking
  ## to right bottom
  LignesDeb <- c(seq(NRows, 1), rep(1, NCols - 1))
  ColsDeb <- c(rep(1, NRows), seq(2, NCols))
  NMatches <- NMatches + sum(vapply(seq_along(LignesDeb), \(index) {
    Coords <- matrix(c(LignesDeb[index] + 0:NRows, ColsDeb[index] + 0:NCols), ncol = 2)
    Coords <- Coords[Coords[, 1] > 0 & Coords[, 1] <= NRows & Coords[, 2] > 0 & Coords[, 2] <= NCols, ]
    VerifVec(Mat[Coords])
  }, numeric(1)))
  ## to left bottom
  LignesDeb <- c(seq(NRows, 1), rep(1, NCols - 1))
  ColsDeb <- c(rep(NCols, NRows), seq(NCols - 1, 1))
  NMatches <- NMatches + sum(vapply(seq_along(LignesDeb), \(index) {
    Coords <- matrix(c(LignesDeb[index] + 0:NRows, ColsDeb[index] - 0:NCols), ncol = 2)
    Coords <- Coords[Coords[, 1] > 0 & Coords[, 1] <= NRows & Coords[, 2] > 0 & Coords[, 2] <= NCols, ]
    VerifVec(Mat[Coords])
  }, numeric(1)))
  return(NMatches)
}
print(paste0("Réponse partie 1 : ", VerifMatrice(WordPuzzle)))


# Part 2 ----

VerifX <- function(Vec) all(Vec[1] == "M", Vec[2] == "M", Vec[3] == "A", Vec[4] == "S", Vec[5] == "S")
VerifMatX <- function(Mat) {
  HautGche <- expand.grid(xx = seq(1, ncol(Mat) - 2), yy = seq(1, nrow(Mat) - 2))
  NXs <- 0
  sum(vapply(seq_len(nrow(HautGche)), \(i) {
    VerifX(Mat[matrix(c(HautGche$yy[i] + c(0, 2, 1, 0, 2), HautGche$xx[i] + c(0, 0, 1, 2, 2)), ncol = 2)]) +
    VerifX(Mat[matrix(c(HautGche$yy[i] + c(0, 0, 1, 2, 2), HautGche$xx[i] + c(0, 2, 1, 0, 2)), ncol = 2)]) +
    VerifX(Mat[matrix(c(HautGche$yy[i] + c(0, 2, 1, 0, 2), HautGche$xx[i] + c(2, 2, 1, 0, 0)), ncol = 2)]) +
    VerifX(Mat[matrix(c(HautGche$yy[i] + c(2, 2, 1, 0, 0), HautGche$xx[i] + c(0, 2, 1, 0, 2)), ncol = 2)])
  }, numeric(1)))
}
print(paste0("Réponse partie 2 : ", VerifMatX(WordPuzzle)))

