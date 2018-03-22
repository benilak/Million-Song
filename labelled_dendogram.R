library(tidyverse)
library(cluster)
songs <- read_csv("C:\\Users\\brega\\Downloads\\test_songs2.csv")

# dendrogram is really only helpful if there is a small sample size
# additionally, only numeric features are allowed for this algorithm
# I also noticed there are a LOT of zeros in the year column

sample <- songs[sample(nrow(songs), 100), ]

sample <- sample %>% 
  select(-c(artist_name, release)) %>%
  filter(year > 0)

# exclude "title" from the distance matrix
songdist <- dist(as.matrix(sample[-1]))
songclusters <- hclust(songdist)

# dendrogram with numbers as labels
plot(songclusters)

# dendrogram with titles as labels
songclusters$labels <- sample$title
plot(songclusters)


# k-means
sample.scaled <- scale(sample)
clusters3 <- kmeans(sample.scaled, 3)
clusplot(sample.scaled, clusters3$cluster, color=TRUE, shade=TRUE, labels=2, lines=0)

