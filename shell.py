import hdf5_getters
import sqlite3
import os
from mmsongsdbtocsvconverter import MMSongsDbToCsvConverter
import pandas
from sklearn.cluster import KMeans


# path = os.path.abspath('millionsongsubset_full\millionsongsubset_full\MillionSongSubset\data')
# converter = MMSongsDbToCsvConverter('test_songs2.csv', ['artist_name', 'title', 'release',  'year', 'tempo',
#                                                         'duration', 'key', 'mode', 'loudness', "artist_hotttnesss", 'time_signature', 'start_of_fade_out'])
# converter.convert_directory(path)

column_names = ['artist_name', 'title', 'release',  'year', 'tempo', 'duration', 'key', 'mode', 'loudness',
                 "artist_hotttnesss", 'time_signature', 'start_of_fade_out']
data_set = pandas.read_csv("test_songs2.csv")
data_set = data_set.drop(['artist_name', 'title', 'release', 'year', 'mode'], axis=1)
print(data_set)


kmeans = KMeans(n_clusters=12)

kmeans.fit(data_set.as_matrix())
print(kmeans.cluster_centers_)




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