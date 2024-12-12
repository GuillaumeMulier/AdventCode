# Day 11 advent of code 2024 #

# Part 1 ----

library(purrr)

Chemin <- "C:/Users/gmulier/Documents/Github/AdventCode/2024"
Input <- readLines(paste0(Chemin, "/Input/day11.txt"))
# Input <- "125 17"
Input <- strsplit(Input, " ")[[1]]

Blink <- function(String) {
  if (as.numeric(String) == 0) {
    return("1")
  } else if (nchar(String) %% 2 == 0) {
    return(as.character(as.numeric(c(substr(String, 1, nchar(String) %/% 2), substr(String, nchar(String) %/% 2 + 1, nchar(String))))))
  } else {
    return(as.character(2024 * as.numeric(String)))
  }
}
Res <- reduce(1:25, \(x, y) unlist(lapply(x, Blink)), .init = Input)
print(paste0("Réponse partie 1 : ", length(Res)))


# Part 2 ----

# Trying memoization
library(memoise)
BlinkRecur <- function(Pierre, IterRest) {
  if (IterRest == 0) {
    return(1)
  } else if (Pierre == "0") {
    return(BlinkRecur("1", IterRest - 1))
    # return(2)
  } else if (nchar(Pierre) %% 2 == 0) {
    # return(3)
    MoitieUne <- BlinkRecur(as.character(as.numeric(substr(Pierre, 1, nchar(Pierre) %/% 2))), IterRest - 1)
    MoitieDeux <- BlinkRecur(as.character(as.numeric(substr(Pierre, 1 + nchar(Pierre) %/% 2, nchar(Pierre)))), IterRest - 1)
    return(MoitieUne + MoitieDeux)
  } else {
    # return(4)
    return(BlinkRecur(as.character(as.numeric(Pierre) * 2024), IterRest - 1))
  }
}
BlinkRecurMem <- memoise(BlinkRecur)
Res <- sum(vapply(Input, \(x) {
  print(paste0("Item n°", match(x, Input), " : ", x))
  BlinkRecurMem(x, 75)
}, numeric(1)))
print(paste0("Réponse partie 2 : ", Res))
# Impossible to finish. I translated it in python

