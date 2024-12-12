# Day 5 advent of code 2024 #

# Part 1 ----

Chemin <- "C:/Users/gmulier/Documents/Github/AdventCode/2024"
Input <- readLines(paste0(Chemin, "/Input/day6.txt"))
MatMusee <- matrix(unlist(strsplit(Input, "")), length(Input), nchar(Input[[1]]), byrow = TRUE)

CheckCollision <- function(x, y, Mat) return(Mat[y, x] == "#")
CheckSortie <- function(x, y, Mat) return(x < 1 | y < 1 | y > nrow(Mat) | x > ncol(Mat))
RealTrajet <- function(Mat) {
  Depart <- which(Mat == "^", arr.ind = TRUE)
  XX <- as.numeric(Depart[1, 2])
  YY <- as.numeric(Depart[1, 1])
  Direction <- c(0, -1)
  DirDir <- "haut"
  NbDoubl <- 0
  DansMusee <- TRUE
  while (DansMusee) {
    XXNew <- XX + Direction[1]
    YYNew <- YY + Direction[2]
    DansMusee <- !CheckSortie(XXNew, YYNew, Mat)
    if (DansMusee) {
      Collision <- CheckCollision(XXNew, YYNew, Mat)
      if (Collision) {
        if (DirDir == "haut") {
          DirDir <- "droite"
          Direction <- c(1, 0)
        } else if (DirDir == "droite") {
          DirDir <- "bas"
          Direction <- c(0, 1)
        } else if (DirDir == "bas") {
          DirDir <- "gauche"
          Direction <- c(-1, 0)
        } else if (DirDir == "gauche") {
          DirDir <- "haut"
          Direction <- c(0, -1)
        }
      } else {
        XX <- XXNew
        YY <- YYNew
        if (Mat[YY, XX] == "^") {
          NbDoubl <- NbDoubl + 1
        } else {
          Mat[YY, XX] <- "^"
          NbDoubl <- 0
        }
        
      }
      if (NbDoubl > 100) break
    }
  }
  return(list(Mat, NbDoubl))
}
CheminGarde <- RealTrajet(MatMusee)
print(paste0("Réponse partie 1 : ", sum(CheminGarde[[1]] == "^")))


# Part 2 ----

# Brute force not quick
# Idea : Reduce the space of search by identifying places that form squares with existing obstacles
SearchLoops <- function(Mat) {
  CasesLibres <- which(Mat == ".", arr.ind = TRUE)
  Res <- vapply(seq_len(nrow(CasesLibres)), \(i) {
    if (i %% 100 == 0) print(paste0(i, "/", nrow(CasesLibres)))
    Mat2 <- Mat
    Mat2[CasesLibres[i, 1], CasesLibres[i, 2]] <- "#"
    CheminTemp <- RealTrajet(Mat2)
    return(CheminTemp[[2]] > 100)
  }, logical(1))
  return(sum(Res))
}
print(paste0("Réponse partie 2 : ", SearchLoops(MatMusee)))

