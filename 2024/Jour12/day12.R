# Day 12 advent of code 2024 #

# Part 1 ----


Chemin <- "C:/Users/gmulier/Documents/Github/AdventCode/2024"
Input <- readLines(paste0(Chemin, "/Input/day12.txt"))
Input <- matrix(unlist(strsplit(Input, "")), nrow = length(Input), ncol = nchar(Input[1]), byrow = TRUE)

GetNeighbors <- function(.row, .col, max_row, max_col, bounded = TRUE) {
  RowsNew <- .row + c(1, 0, -1, 0)
  ColsNew <- .col + c(0, 1, 0, -1)
  IndiceOk <- (RowsNew > 0) & (RowsNew <= max_row) & (ColsNew > 0) & (ColsNew <= max_col)
  if (bounded) {
    return(matrix(c(RowsNew, ColsNew), ncol = 2)[IndiceOk, ])
  } else {
    return(matrix(c(RowsNew, ColsNew), ncol = 2))
  }
}
FloodFill <- function(rr, cc, .Mat) {
  Res <- matrix(c(rr, cc), ncol = 2)
  ListeIni <- GetNeighbors(rr, cc, nrow(.Mat), ncol(.Mat))
  while (nrow(ListeIni) > 0) {
    RowExam <- ListeIni[1, 1]
    ColExam <- ListeIni[1, 2]
    if (any(RowExam == Res[, 1] & ColExam == Res[, 2])) {
      # Do nothing, could be optimized I think by checking before putting values in list
    } else if (.Mat[RowExam, ColExam] == .Mat[rr, cc]) {
      Res <- rbind(Res, matrix(c(RowExam, ColExam), ncol = 2))
      Temp <- GetNeighbors(RowExam, ColExam, nrow(.Mat), ncol(.Mat))
      ListeIni <- rbind(ListeIni, Temp)
    }
    ListeIni <- matrix(ListeIni[-1, ], ncol = 2)
  }
  return(Res)
}
FindAllRegions <- function(.Mat) {
  .MatVis <- matrix(TRUE, nrow(.Mat), ncol(.Mat))
  ListeRegions <- list()
  while (sum(.MatVis) > 0) {
    Ex <- which(.MatVis, arr.ind = TRUE)[1, ]
    Region <- FloodFill(Ex[1], Ex[2], .Mat)
    ListeRegions <- append(ListeRegions, list(Region))
    .MatVis[Region] <- FALSE
  }
  return(ListeRegions)
}
CalcPrix <- function(Region) {
  Area <- nrow(Region)
  Perimetre <- 0
  VecReg <- apply(Region, 1, paste, collapse = "-")
  for (i in seq_len(Area)) {
    Voisins <- GetNeighbors(Region[i, 1], Region[i, 2], 0, 0, FALSE)
    Perimetre <- Perimetre + sum(!apply(Voisins, 1, paste, collapse = "-") %in% VecReg)
  }
  return(Area * Perimetre)
}
Res <- FindAllRegions(Input)
Res <- vapply(Res, CalcPrix, numeric(1))
print(paste0("Réponse partie 1 : ", sum(Res)))


# Part 2 ----

CalcPrix2 <- function(Region) {
  Area <- nrow(Region)
  VecReg <- apply(Region, 1, paste, collapse = "-")
  FindCorners <- function(rr, cc, VecReg) {
    Matrice <- matrix(c(rr + c(-.5, .5, .5, -.5), cc + c(-.5, -.5, .5, .5), rr + c(-.5, -.5, .5, .5), cc + c(.5, -.5, -.5, .5)), ncol = 4)
    CoinH <- !paste0(rr - 1, "-", cc) %in% VecReg
    CoinG <- !paste0(rr, "-", cc - 1) %in% VecReg
    CoinB <- !paste0(rr + 1, "-", cc) %in% VecReg
    CoinD <- !paste0(rr, "-", cc + 1) %in% VecReg
    return(Matrice[c(CoinH, CoinG, CoinB, CoinD), ])
  }
  Contour <- do.call("rbind", lapply(seq_len(Area), \(i) FindCorners(Region[i, 1], Region[i, 2], VecReg)))
  ContourChar <- apply(Contour, 1, \(x) paste0(x[1], "-", x[2], "/", x[3], "-", x[4]))
  Coins <- 0
  for (i in seq_len(nrow(Contour))) {
    PtGauche <- gsub("(.*)/.*", "\\1", ContourChar[i])
    if (any(grepl(paste0("^", PtGauche, "|/", PtGauche), ContourChar[-i]))) {
      Seg1R <- Contour[i, c(1, 3)]
      Seg1C <- Contour[i, c(2, 4)]
      Seg2R <- Contour[-i, ][grepl(paste0("^", PtGauche, "|/", PtGauche), ContourChar[-i]), c(1, 3)]
      Seg2C <- Contour[-i, ][grepl(paste0("^", PtGauche, "|/", PtGauche), ContourChar[-i]), c(2, 4)]
      if (is.matrix(Seg2C)) {
        DotProd <- diff(Seg1R) * (Seg2R[, 2] - Seg2R[, 1]) + diff(Seg1C) * (Seg2C[, 2] - Seg2C[, 1])
        if (any(DotProd == 0)) {
          Coins <- Coins + .5
        }
      } else {
        DotProd <- diff(Seg1R) * diff(Seg2R) + diff(Seg1C) * diff(Seg2C)
        if (DotProd == 0) {
          Coins <- Coins + 1
        }
      }
    }
    PtDroit <- gsub(".*/(.*)", "\\1", ContourChar[i])
    if (any(grepl(paste0("^", PtDroit, "|/", PtDroit), ContourChar[-i]))) {
      Seg1R <- Contour[i, c(1, 3)]
      Seg1C <- Contour[i, c(2, 4)]
      Seg2R <- Contour[-i, ][grepl(paste0("^", PtDroit, "|/", PtDroit), ContourChar[-i]), c(1, 3)]
      Seg2C <- Contour[-i, ][grepl(paste0("^", PtDroit, "|/", PtDroit), ContourChar[-i]), c(2, 4)]
      if (is.matrix(Seg2C)) {
        DotProd <- diff(Seg1R) * (Seg2R[, 2] - Seg2R[, 1]) + diff(Seg1C) * (Seg2C[, 2] - Seg2C[, 1])
        if (any(DotProd == 0)) {
          Coins <- Coins + .5
        }
      } else {
        DotProd <- diff(Seg1R) * diff(Seg2R) + diff(Seg1C) * diff(Seg2C)
        if (DotProd == 0) {
          Coins <- Coins + 1
        }
      }
    }
    ContourChar[i] <- ""
  }
  return(Area * Coins)
}
Res <- FindAllRegions(Input)
Res <- vapply(Res, CalcPrix2, numeric(1))
print(paste0("Réponse partie 2 : ", sum(Res)))

