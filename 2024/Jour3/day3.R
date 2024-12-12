# Day 3 advent of code 2024 #

# Part 1 ----

Chemin <- "C:/Users/gmulier/Documents/Github/AdventCode/2024"
Input <- readLines(paste0(Chemin, "/Input/day3.txt"))

ExtractInstructions <- function(x, Regexp) {
  Coords <- gregexpr(Regexp, x)
  ListeInst <- lapply(seq_along(Coords), \(index) {
    Debut <- as.numeric(Coords[[index]])
    if (all(Debut == -1)) {
      return(NULL)
    } else {
      Longueur <- as.numeric(attr(Coords[[index]],"match.length"))
      return(vapply(seq_along(Debut), \(i) substr(x[[index]], Debut[i], Debut[i] + Longueur[i] - 1), character(1)))
    }
  })
  return(unlist(ListeInst))
}
Instructions <- ExtractInstructions(Input, "mul\\(\\d{1,3},\\d{1,3}\\)")
Nbs <- vapply(Instructions, \(x) as.numeric(gsub("mul\\((\\d{1,3}),(\\d{1,3})\\)", "\\1", x)) * as.numeric(gsub("mul\\((\\d{1,3}),(\\d{1,3})\\)", "\\2", x)), numeric(1))
print(paste0("Réponse partie 1 : ", sum(Nbs)))


# Part 2 ----

Instructions <- ExtractInstructions(Input, "mul\\(\\d{1,3},\\d{1,3}\\)|do\\(\\)|don't\\(\\)")
Resultat <- 0
Multiplicateur <- 1
for (inst in Instructions) {
  if (inst == "do()") {
    Multiplicateur <- 1
  } else if (inst == "don't()") {
    Multiplicateur <- 0
  } else {
    Resultat <- Resultat + Multiplicateur * as.numeric(gsub("mul\\((\\d{1,3}),(\\d{1,3})\\)", "\\1", inst)) * as.numeric(gsub("mul\\((\\d{1,3}),(\\d{1,3})\\)", "\\2", inst))
  }
}
print(paste0("Réponse partie 2 : ", Resultat))

