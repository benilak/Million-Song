import hdf5_getters
import sqlite3
import os
from mmsongsdbtocsvconverter import MMSongsDbToCsvConverter
import pandas
from sklearn.cluster import KMeans
from sklearn import preprocessing
from sklearn.cluster import AgglomerativeClustering
from scipy.cluster.hierarchy import dendrogram, linkage
from scipy.cluster.hierarchy import fcluster
import matplotlib.pyplot as plt
import numpy as np
import csv



# path = os.path.abspath('C:\\Users\Landon\Desktop\millionsongsubset_full\millionsongsubset_full\MillionSongSubset\data')
# converter = MMSongsDbToCsvConverter('test_songsFinal.csv', ['artist_name', 'title', 'release',  'year', 'tempo',
#                                                         'duration', 'key', 'mode', 'loudness', "artist_hotttnesss",
#                                                         'time_signature', 'start_of_fade_out', 'end_of_fade_in', 'artist_terms'])
# converter.convert_directory(path)

column_names = ['artist_name', 'title', 'release',  'year', 'tempo', 'duration', 'key', 'mode', 'loudness',
                 "artist_hotttnesss", 'time_signature', 'start_of_fade_out']
data_set = pandas.read_csv("/Users/parkerweech/Desktop/Education/Winter_2018/Machine_Learning_And_Data_Mining/Group_Assignment/Million-Song-master_3:29_212/test_songs2.csv")
artist_names = data_set["artist_name"]
sql = "SELECT COALESCE(artist_name, '') || ', ' || COALESCE(title, '') as song from songs"
conn = sqlite3.connect('/Users/parkerweech/Desktop/Education/Winter_2018/Machine_Learning_And_Data_Mining/Group_Assignment/Million-Song-master_3:29_212/songs_subset.db')
cursor = conn.cursor()

data_labels = pandas.read_sql(sql, conn, )
# print(data_labels)
conn.close
data_set = data_set.drop(['artist_name', 'title', 'release', 'year', 'mode'], axis=1)

# print(data_set)
data_array = data_set.as_matrix()
# print("before scaling:")
# print(data_array[:10, ])
scaler = preprocessing.StandardScaler().fit(data_array)
data_array = scaler.transform(data_array)
# print("after scaling:")
# print(data_array[:10, ])
cluster = linkage(data_array, 'single')
# calculate full dendrogram
# plt.figure()
# plt.title('Hierarchical Clustering Dendrogram')
# plt.xlabel('sample index')
# plt.ylabel('distance')
clustered_songs = fcluster(
    cluster,
    0
)

print(len(clustered_songs))
print(clustered_songs[2])

csvfile = "/Users/parkerweech/Desktop/Education/Winter_2018/Machine_Learning_And_Data_Mining/Group_Assignment/Million-Song-master_3:29_212/fcluster.csv"
with open(csvfile, "w") as output:
    writer = csv.writer(output, lineterminator='\n')
    for val in clustered_songs:
        writer.writerow([val])

# plt.show()
# artist_list = list(clustered_songs)
# for song in artist_list[0:5]:
#     print(song)
# artist_flat_cluster = fcluster(cluster, t=.1)
# print(artist_flat_cluster[0:5])






# kmeans = KMeans(n_clusters=12)
#
# kmeans.fit(data_set.as_matrix())
# print(kmeans.cluster_centers_)




# open file so we can extract info
# h5 = hdf5_getters.open_h5_file_read(os.path.abspath("example_song_files/example3.h5"))
#
# duration = hdf5_getters.get_duration(h5)
# number = hdf5_getters.get_num_songs(h5)
# artist = hdf5_getters.get_artist_name(h5)
# title = hdf5_getters.get_title(h5)
# genres = hdf5_getters.get_artist_terms(h5)
# genre_weight = hdf5_getters.get_artist_terms_weight(h5)
# key = hdf5_getters.get_key(h5)
#
# print("Title: {} Artist: {} genres: {}".format(title, artist, genres))
# print(key)

# alternative option, using a SQLite DB
# conn = sqlite3.connect('example_song_files/subset_track_metadata.db')
# cursor = conn.cursor()
# cursor.execute("""SELECT title, artist_name FROM songs""")
# results = cursor.fetchall()
# for result in results:
#     print(result)
# conn.close()
# h5.close()