library(cluster)

data <- state.x77
data <- NULL

distance <- dist(as.matrix(data))

data <- read.csv("test_songs2.csv")
head(data, n=10)
help(read.csv)

edited_data <- subset(data, select = -c(artist_name, title, release, year, mode, tempo))
head(edited_data, n=10)
sapply(edited_data, class)
edited_data <- scale(edited_data)
sub_data <- head(edited_data, n=200)
View(edited_data)


distance <- dist(as.matrix(sub_data))

hierarchicalCluster <- hclust(distance)

plot(hierarchicalCluster)
