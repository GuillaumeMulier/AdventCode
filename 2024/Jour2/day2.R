# Day 2 advent of code 2024 #

# Part 1 ----

Chemin <- "C:/Users/gmulier/Documents/Github/AdventCode/2024"
Input <- readLines(paste0(Chemin, "/Input/day2.txt"))
Input <- lapply(strsplit(Input, " "), as.numeric)
IsSafe <- function(x) {
  Differences <- diff(x)
  return(all(sign(Differences) == sign(Differences)[1]) & all(abs(Differences) %in% c(1, 2, 3)))
}
print(paste0("Réponse partie 1 : ", sum(vapply(Input, IsSafe, logical(1)))))


# Part 2 ----

TestRemove <- function(x) {
  return(any(vapply(seq_along(x), \(index) IsSafe(x[-index]), logical(1))))
}
print(paste0("Réponse partie 2 : ", sum(vapply(Input, TestRemove, logical(1)))))

