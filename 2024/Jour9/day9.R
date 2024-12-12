# Day 9 advent of code 2024 #

# Part 1 ----

Chemin <- "C:/Users/gmulier/Documents/Github/AdventCode/2024"
Input <- readLines(paste0(Chemin, "/Input/day9.txt"))

CreateDiskmap <- function(String) {
  String <- strsplit(String, "")[[1]]
  Res <- numeric(0)
  for (n in seq_along(String)) {
    if ((n - 1) %% 2 == 0) {
      Res <- c(Res, rep((n - 1) %/% 2, as.numeric(String[[n]])))
    } else {
      Res <- c(Res, rep(-1, as.numeric(String[[n]])))
    }
  }
  return(Res)
}
Amphipod <- function(VecFrag) {
  PlacesNonNa <- rev(which(VecFrag > 0))
  for (i in seq_along(VecFrag)) {
    if ((VecFrag[i] < 0) & i < PlacesNonNa[1]) {
      VecFrag[i] <- VecFrag[PlacesNonNa[1]]
      VecFrag[PlacesNonNa[1]] <- -1
      PlacesNonNa <- PlacesNonNa[-1]
    }
  }
  return(VecFrag)
}
CheckSum <- function(VecDefrag) sum(as.numeric(VecDefrag) * (VecDefrag >= 0) * (seq_along(VecDefrag) - 1), na.rm = TRUE)
Resultat <- CreateDiskmap(Input) |> Amphipod() |> CheckSum()
print(paste0("Réponse partie 1 : ", Resultat))


# Part 2 ----

AmphipodWhole <- function(VecFrag) {
  DfGroupes <- data.frame(val = rle(VecFrag)$values, nb = rle(VecFrag)$lengths)
  DfGroupes$pos_mini <- cumsum(c(1, DfGroupes$nb[-nrow(DfGroupes)]))
  DfGroupes$pos_maxi <- cumsum(DfGroupes$nb)
  DfPresent <- DfGroupes[DfGroupes$val >= 0, ]
  DfPresent <- DfPresent[nrow(DfPresent):1, ]
  DfAbsent <- DfGroupes[DfGroupes$val < 0, ]
  for (i in seq_len(nrow(DfPresent))) {
    LongueurRech <- DfPresent$nb[i]
    Maxi <- DfPresent$pos_mini[i]
    if (any(DfAbsent$nb >= LongueurRech & DfAbsent$pos_maxi < Maxi)) {
      PlacePossible <- which(DfAbsent$nb >= LongueurRech & DfAbsent$pos_maxi < Maxi)[1]
      Rempl <- DfPresent[i, ]
      Rempl$val <- -1
      DfPresent$pos_mini[i] <- DfAbsent$pos_mini[PlacePossible]
      DfPresent$pos_maxi[i] <- DfPresent$pos_mini[i] + DfPresent$nb[i] - 1
      DfAbsent$nb[PlacePossible] <- DfAbsent$nb[PlacePossible] - DfPresent$nb[i]
      DfAbsent$pos_mini[PlacePossible] <- DfPresent$pos_maxi[i] + 1
      DfAbsent <- rbind(DfAbsent, Rempl)
    }
  }
  DfGroupes <- rbind(DfPresent, DfAbsent[DfAbsent$nb > 0, ])
  DfGroupes <- DfGroupes[order(as.numeric(DfGroupes$pos_mini)), ]
  return(rep(DfGroupes$val, DfGroupes$nb))
}
Resultat <- CreateDiskmap(Input) |> AmphipodWhole() |> CheckSum()
print(paste0("Réponse partie 2 : ", Resultat))
