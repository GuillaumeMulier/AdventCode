# Day 1 advent of code 2024 #

# Part 1 ----

Chemin <- "C:/Users/gmulier/Documents/Github/AdventCode/2024"
Input <- read.table(paste0(Chemin, "/Input/day1.txt"), header = FALSE)
print(paste0("Réponse partie 1 : ", sum(abs(sort(Input$V1) - sort(Input$V2)))))


# Part 2 ----

print(paste0("Réponse partie 2 : ", sum(vapply(Input$V1, \(rech) rech * sum(Input$V2 == rech), numeric(1)))))

