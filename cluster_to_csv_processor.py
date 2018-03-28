import sqlite3
import pandas
from sklearn import preprocessing
from scipy.cluster.hierarchy import dendrogram, linkage
from scipy.cluster.hierarchy import fcluster
import matplotlib.pyplot as plt
import numpy as np
from sklearn.preprocessing import LabelEncoder


column_names = ['artist_name', 'title', 'release',  'year', 'tempo', 'duration', 'key', 'mode', 'loudness',
                 "artist_hotttnesss", 'time_signature', 'start_of_fade_out']
data_set = pandas.read_csv("test_songsFinal.csv")

sql = "SELECT COALESCE(artist_name, '') || ', ' || COALESCE(title, '') as song from songs"
conn = sqlite3.connect('songs_subset.db')
cursor = conn.cursor()

data_labels = pandas.read_sql(sql, conn)
labels_list = data_labels['song'].tolist()
conn.close

data_set = data_set.drop(['artist_name', 'title', 'release', 'year', 'mode'], axis=1)

# label encode the genres
encoder = LabelEncoder()
print(data_set['artist_terms'])
encoder.fit(data_set['artist_terms'])
data_set['artist_terms'] = encoder.transform(data_set['artist_terms'])
print(data_set['artist_terms'])

# scale the data set
# store the genres in another variable, we don't want to scale them
artist_terms = data_set['artist_terms']
# print(artist_terms.shape)
data_set = data_set.drop(['artist_terms'], axis=1)

# scale the rest of the data
data_array = data_set.as_matrix()
scaler = preprocessing.StandardScaler().fit(data_array)
data_array = scaler.transform(data_array)

# now combine the genre data back into the rest of the data
artist_terms = artist_terms.as_matrix()
data_combined = np.column_stack((data_array, artist_terms))
print(data_combined[:3])

# cluster using single linkage
cluster = linkage(data_combined, 'single')
# # calculate full dendrogram
# plt.figure()
# plt.title('Hierarchical Clustering Dendrogram')
# plt.xlabel('sample index')
# plt.ylabel('distance')
clustered_songs = dendrogram(
    cluster,
    orientation="right",
    truncate_mode="none",
    leaf_font_size=5.,  # font size for the x axis labels
    labels=data_labels.iloc(),
    get_leaves=True
)
# plt.show()
artist_list = list(clustered_songs['ivl'])
file = open('cluster_song_ids.txt', 'w')
print("writing song ids to file")
for song in artist_list:
     file.write(str(song.name) + '\n')
file.close()