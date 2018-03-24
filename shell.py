import hdf5_getters
import sqlite3
import os
from mmsongsdbtocsvconverter import MMSongsDbToCsvConverter
import pandas
from sklearn.cluster import KMeans
from sklearn import preprocessing
from sklearn.cluster import AgglomerativeClustering
from scipy.cluster.hierarchy import dendrogram, linkage
import matplotlib.pyplot as plt
import numpy as np


# path = os.path.abspath('C:\\Users\Landon\Desktop\millionsongsubset_full\millionsongsubset_full\MillionSongSubset\data')
# converter = MMSongsDbToCsvConverter('test_songsFinal.csv', ['artist_name', 'title', 'release',  'year', 'tempo',
#                                                         'duration', 'key', 'mode', 'loudness', "artist_hotttnesss",
#                                                         'time_signature', 'start_of_fade_out', 'end_of_fade_in', 'artist_terms'])
# converter.convert_directory(path)

column_names = ['artist_name', 'title', 'release',  'year', 'tempo', 'duration', 'key', 'mode', 'loudness',
                 "artist_hotttnesss", 'time_signature', 'start_of_fade_out']
data_set = pandas.read_csv("test_songs2.csv")
artist_names = data_set["artist_name"]
print(artist_names[:10])
data_set = data_set.drop(['artist_name', 'title', 'release', 'year', 'mode'], axis=1)

# print(data_set)
data_array = data_set.as_matrix()
# print("before scaling:")
# print(data_array[:10, ])
scaler = preprocessing.StandardScaler().fit(data_array)
data_array = scaler.transform(data_array)
# print("after scaling:")
# print(data_array[:10, ])

cluster = linkage(data_array[:5000, ], 'complete')
# calculate full dendrogram
plt.figure()
plt.title('Hierarchical Clustering Dendrogram')
plt.xlabel('sample index')
plt.ylabel('distance')
dendrogram(
    cluster,
    orientation="right",
    p=9,
    truncate_mode="level",
    leaf_font_size=5.,  # font size for the x axis labels
    labels=artist_names[:5000].iloc()
)
plt.show()


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