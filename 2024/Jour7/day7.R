# Day 7 advent of code 2024 #

# Part 1 ----

Chemin <- "C:/Users/gmulier/Documents/Github/AdventCode/2024"
Input <- readLines(paste0(Chemin, "/Input/day7.txt"))
Input <- do.call("rbind", strsplit(Input, ": "))

CheckPossible <- function(Somme, Termes) {
  Termes <- strsplit(Termes, " ")[[1]]
  Operateurs <- expand.grid(lapply(seq_len(length(Termes) - 1), \(x) c("+", "*")))
  Operateurs$der <- ""
  Operations <- apply(Operateurs, 1, \(x) paste(Termes, ")", x, collapse = " "))
  Operations <- paste0(strrep("(", length(Termes)), Operations)
  return(Somme * (any(Somme == vapply(Operations, \(x) eval(parse(text = x)), numeric(1)))))
}
Res <- vapply(seq_len(nrow(Input)), \(i) CheckPossible(as.numeric(Input[i, 1]), Input[i, 2]), numeric(1))
print(paste0("Réponse partie 1 : ", sum(Res)))


# Part 2 ----

CheckPossible2 <- function(Somme, Termes) {
  Termes <- strsplit(Termes, " ")[[1]]
  Operateurs <- expand.grid(lapply(seq_len(length(Termes) - 1), \(x) c("+", "*", "||")))
  Resultats <- apply(Operateurs, 1, \(x) {
    Res <- Termes[1]
    for (i in seq_along(x)) {
      if (x[i] == "+") {
        Res <- as.numeric(Res) + as.numeric(Termes[i + 1])
      } else if (x[i] == "*") {
        Res <- as.numeric(Res) * as.numeric(Termes[i + 1])
      } else {
        Res <- paste0(Res, Termes[i + 1])
      }
    }
    return(Res)
  })
  return(Somme * any(Resultats == Somme))
}
# Only check for results that are not checked in part 1 to speed up things
# But still slow...
Res2 <- vapply(seq_len(nrow(Input)), \(i) {
  if (i %% 50 == 0) print(i)
  if (Res[i] != 0) {
    return(Res[i])
  } else {
    return(CheckPossible2(as.numeric(Input[i, 1]), Input[i, 2]))
  }
}, numeric(1))
print(paste0("Réponse partie 2 : ", sum(Res2)))
