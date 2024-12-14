# Day 13 advent of code 2024 #

# Part 1 ----


Chemin <- "C:/Users/gmulier/Documents/Github/AdventCode/2024"
Input <- readLines(paste0(Chemin, "/Input/day13.txt"))
# Input <- "Button A: X+94, Y+34
# Button B: X+22, Y+67
# Prize: X=8400, Y=5400
# 
# Button A: X+26, Y+66
# Button B: X+67, Y+21
# Prize: X=12748, Y=12176
# 
# Button A: X+17, Y+86
# Button B: X+84, Y+37
# Prize: X=7870, Y=6450
# 
# Button A: X+69, Y+23
# Button B: X+27, Y+71
# Prize: X=18641, Y=10279"
# Input <- strsplit(Input, "\n")[[1]]
Input <- strsplit(paste(Input, collapse = "@"), "@@")[[1]]

ExtractInputs <- function(String) {
  Regex <- "^Button A: X([\\+0-9]+), Y([\\+0-9]+)@Button B: X([\\+0-9]+), Y([\\+0-9]+)@Prize: X=([0-9]+), Y=([0-9]+)$"
  Ax <- as.numeric(gsub(Regex, "\\1", String))
  Ay <- as.numeric(gsub(Regex, "\\2", String))
  Bx <- as.numeric(gsub(Regex, "\\3", String))
  By <- as.numeric(gsub(Regex, "\\4", String))
  X <- as.numeric(gsub(Regex, "\\5", String))
  Y <- as.numeric(gsub(Regex, "\\6", String))
  return(c(Ax, Ay, Bx, By, X, Y))
}
# Integer programming
library(lpSolve)
MinTokens <- function(Inputs) {
  f.obj <- c(3, 1)
  f.con <- matrix(Inputs[1:4], 2, 2)
  f.con <- rbind(f.con, matrix(c(1, 0, 0, 1), 2, 2))
  f.dir <- c("=", "=", "<=", "<=")
  f.rhs <- c(Inputs[5:6], 100, 100)
  Res <- lp("min", f.obj, f.con, f.dir, f.rhs, all.int = TRUE)
  return(Res$objval)
}
Res <- vapply(Input, \(s) MinTokens(ExtractInputs(s)), numeric(1))
print(paste0("Réponse partie 1 : ", sum(Res)))


# Part 2 ----

# lpSolve fails with high numbers so going for solving equations
# Minimization was a hoax there is only one solution
# ax*a+bx*b=x // ay*a+by*b=y
# (1) - bx/by*(2)
# ax*a+bx*b-bx/by*ay*a-bx/by*by*b= a * (ax - ay * bx / by) = x - y * bx / by
# (1) - ax/ay*(2)
# ax*a+bx*b-ax/ay*ay*a-ax/ay*by*b = b * (bx - by * ax / ay) = x - y * ax / ay
MinTokens2 <- function(Inputs) {
  a <- (Inputs[5] * Inputs[4] - Inputs[6] * Inputs[3]) / (Inputs[1] * Inputs[4] - Inputs[2] * Inputs[3])
  b <- (Inputs[5] * Inputs[2] - Inputs[6] * Inputs[1]) / (Inputs[3] * Inputs[2] - Inputs[4] * Inputs[1])
  if (((floor(a) * Inputs[1] + floor(b) * Inputs[3]) == Inputs[5]) & ((floor(a) * Inputs[2] + floor(b) * Inputs[4]) == Inputs[6])) {
    return(3 * floor(a) + floor(b))
  } else {
    return(0)
  }
}
Res <- vapply(Input, \(s) {
  Temp <- ExtractInputs(s)
  Temp[5:6] <- Temp[5:6] + 10000000000000
  return(MinTokens2(Temp))
}, numeric(1))
print(paste0("Réponse partie 2 : ", sum(Res)))

