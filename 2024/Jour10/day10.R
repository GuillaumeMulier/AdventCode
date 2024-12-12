# Day 10 advent of code 2024 #

# Part 1 ----

Chemin <- "C:/Users/gmulier/Documents/Github/AdventCode/2024"
Input <- readLines(paste0(Chemin, "/Input/day10.txt"))
Input <- matrix(as.numeric(unlist(strsplit(Input, ""))), length(Input), nchar(Input[1]), byrow = TRUE)

GetNeighbors <- function(.row, .col, .val, max_row, max_col) {
  RowsNew <- .row + c(1, 0, -1, 0)
  ColsNew <- .col + c(0, 1, 0, -1)
  IndiceOk <- (RowsNew > 0) & (RowsNew <= max_row) & (ColsNew > 0) & (ColsNew <= max_col)
  return(matrix(c(RowsNew, ColsNew, rep(.val, 4)), ncol = 3)[IndiceOk, ])
}
CountTrail <- function(.row, .col, .Mat, .val, part1 = TRUE) {
  Compte <- matrix(nrow = 0, ncol = 2)
  NRows <- nrow(.Mat)
  NCols <- ncol(.Mat)
  WaitingRoom <- GetNeighbors(.row, .col, .val, NRows, NCols)
  while (nrow(WaitingRoom) > 0) {
    rr <- WaitingRoom[1, 1]
    cc <- WaitingRoom[1, 2]
    vv <- WaitingRoom[1, 3]
    if (vv == 8 & .Mat[rr, cc] == 9) {
      Compte <- rbind(Compte, matrix(c(rr, cc), ncol = 2))
    } else if (.Mat[rr, cc] != (vv + 1)) {
      # On ne fait rien
    } else if (.Mat[rr, cc] == (vv + 1)) {
      WaitingRoom <- rbind(WaitingRoom, GetNeighbors(rr, cc, .Mat[rr, cc], NRows, NCols))
    }
    # Update queue
    WaitingRoom <- matrix(WaitingRoom[-1, ], ncol = 3)
  }
  if (part1) {
    Compte <- matrix(Compte[!duplicated(apply(Compte, 1, paste, collapse = "-")), ], ncol = 2)
  }
  return(nrow(Compte))
}
PosDepart <- which(Input == 0, arr.ind = TRUE)
Res <- vapply(seq(1, nrow(PosDepart)), \(i) CountTrail(PosDepart[i, 1], PosDepart[i, 2], Input, 0, TRUE), numeric(1))
print(paste0("Réponse partie 1 : ", sum(Res)))


# Part 2 ----

Res <- vapply(seq(1, nrow(PosDepart)), \(i) CountTrail(PosDepart[i, 1], PosDepart[i, 2], Input, 0, FALSE), numeric(1))
print(paste0("Réponse partie 2 : ", sum(Res)))

