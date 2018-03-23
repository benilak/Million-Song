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


# sample with a handful of artists
# (the same process can be used to select specific genres/etc.)
sample.artists <- songs %>%
  filter(artist_name %in% c("'Usher'", "'Gorillaz'", "'Korn'","'30 Seconds To Mars'", 
                            "'Devo'", "'Maroon 5'", "'NOFX'", "'Sade'"),
         year > 0) %>%
  select(-c(title, release))
# exclude artist_name from the distance matrix
sample.artists.dist <- dist(as.matrix(sample.artists[-1]))
artist.clusters <- hclust(sample.artists.dist)
# set the labels as the artist names
artist.clusters$labels <- sample.artists$artist_name
plot(artist.clusters)


# k-means with the ame artists above
artists.scaled <- scale(sample.artists[-1])
artists.clusters <- kmeans(artists.scaled, 8)
clusplot(artists.scaled, artists.clusters$cluster, color=TRUE, shade=TRUE, labels=2, lines=0)
# this adds a column to the dataframe indicating the cluster each song was put into
# (it reveals the clustering didn't go very well)
sample.artists$cluster <- artists.clusters$cluster

# I think this means we may have some features that are ditracting from clustering songs
# according to similarity, or that we are missing some features that would help to
# cluster according to similarity
