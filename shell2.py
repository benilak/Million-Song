import hdf5_getters
import sqlite3
import os
from mmsongsdbtocsvconverter import MMSongsDbToCsvConverter
import pandas
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D


# path = os.path.abspath('millionsongsubset_full\millionsongsubset_full\MillionSongSubset\data')
# converter = MMSongsDbToCsvConverter('test_songs2.csv', ['artist_name', 'title', 'release',  'year', 'tempo',
#                                                         'duration', 'key', 'mode', 'loudness', "artist_hotttnesss", 'time_signature', 'start_of_fade_out'])
# converter.convert_directory(path)

column_names = ['artist_name', 'title', 'release',  'year', 'tempo', 'duration', 'key', 'mode', 'loudness',
                 "artist_hotttnesss", 'time_signature', 'start_of_fade_out']
data_set = pandas.read_csv("/Users/parkerweech/Desktop/Education/Winter_2018/Machine_Learning_And_Data_Mining/Group_Assignment/Million-Song-master_3:20_345/test_songs2.csv")
data_set = data_set.drop(['artist_name', 'title', 'release', 'year', 'mode'], axis=1)
print(data_set)

data_array = data_set.values

kmeans = KMeans(n_clusters=12)

kmeans.fit(data_set.as_matrix())
#print(kmeans.cluster_centers_)
# 
f1 = data_set['tempo'].values
f2 = data_set['duration'].values
f3 = data_set['loudness'].values
X = np.array(list(zip(f1, f2)))

kmeans.fit(data_array)

labels = kmeans.predict(data_array)

C = kmeans.cluster_centers_

fig = plt.figure()
ax = Axes3D(fig)
ax.scatter(f1,f2,f3)

ax.set_xlabel('Tempo')
ax.set_ylabel('Duration')
ax.set_zlabel('Loudness')

plt.show()

np.set_printoptions(threshold=8)
print(f3)

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