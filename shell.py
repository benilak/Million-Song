import hdf5_getters
import sqlite3
# open file so we can extract info
h5 = hdf5_getters.open_h5_file_read("example_song_files/example3.h5")


duration = hdf5_getters.get_duration(h5)
number = hdf5_getters.get_num_songs(h5)
artist = hdf5_getters.get_artist_name(h5)
title = hdf5_getters.get_title(h5)
genres = hdf5_getters.get_artist_terms(h5)
genre_weight = hdf5_getters.get_artist_terms_weight(h5)
key = hdf5_getters.get_key(h5)

print("Title: {} Artist: {} genres: {}".format(title, artist, genres))
print(key)

# alternative option, using a SQLite DB
conn = sqlite3.connect('example_song_files/subset_track_metadata.db')
cursor = conn.cursor()
cursor.execute("""SELECT title, artist_name FROM songs""")
results = cursor.fetchall()
for result in results:
    print(result)
conn.close()
h5.close()