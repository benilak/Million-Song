import tkinter as tk
from tkinter import font as tkfont
from tkinter import messagebox
from tkinter import *
import pandas
import sqlite3
import webbrowser
import os

# DATA_SET = pandas.read_csv("test_songsFinal.csv")
# ARTIST_NAMES = DATA_SET["artist_name"].iloc()


class SongPredictor():
    """The driver class of the program"""
    def __init__(self):
        """default constructor"""
        self.clustered_ids = None
        self.main_menu = Main_Menu()
        self.create_db_file()
        self.load_cluster_ids()

    def create_db_file(self):
        conn = sqlite3.connect('songs_subset.db')
        cursor = conn.cursor()

        # use pandas to convert the dataframe into a DB table, which is AWESOME!!!
        # DATA_SET.to_sql("songs", conn, if_exists="replace")

        # the old fashioned way
        # cursor.execute("""CREATE TABLE IF NOT EXISTS SONGS(
        #                   song_id INTEGER PRIMARY KEY,
        #                   artist_name text,
        #                   title text,
        #                   release text,
        #                   year int,
        #                   tempo double,
        #                   duration double,
        #                   key int,
        #                   mode int,
        #                   loudness double,
        #                   artist_hotttnesss double,
        #                   time_signature int,
        #                   start_of_fade_out double,
        #                   end_of_fade_in double,
        #                   artist_genre text
        #               );""")

        conn.close()

    def load_cluster_ids(self):
        with open("../cluster_song_ids.txt") as f:
            self.clustered_ids = f.readlines()
        self.clustered_ids = [x.strip() for x in self.clustered_ids]
        print(self.clustered_ids[:5])

    def get_song_id(self, song, artist):
        conn = sqlite3.connect('songs_subset.db')
        cursor = conn.cursor()
        cursor.execute("""SELECT "index" from songs where artist_name = ? and title = ?""", (artist.strip(), song.strip(), ))
        id = cursor.fetchone()
        print("id is = " + str(id[0]))
        conn.close()
        return id[0]

    def get_recommendations(self, song, artist):
        print(song + " " + artist)
        song_id = self.get_song_id(song, artist)
        cluster_index = self.clustered_ids.index(str(song_id))
        print(cluster_index)
        # get 6 closest songs to selected song
        rec_song_ids = self.clustered_ids[cluster_index - 3:cluster_index] + self.clustered_ids[cluster_index + 1: cluster_index + 4]
        # convert string ids to ints
        results = [int(i) for i in rec_song_ids]
        self.main_menu.populate_recommendation_page(results)



class Main_Menu(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")
        self.minsize(height="300", width="500")


        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (SearchPage, SongPage, RecommendPage, StartPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

    def display_artist_songs(self, artist):
        # print(artist)
        conn = sqlite3.connect('songs_subset.db')
        conn.row_factory = lambda cursor, row: row[0]
        cursor = conn.cursor()
        # get songs that match artist
        sql = "SELECT title from songs WHERE artist_name = '" + artist.strip() + "' ORDER BY title"
        # print(sql)
        cursor.execute(sql)
        songs = cursor.fetchall()
        # print(songs)
        # first reset the song results field
        frame = self.frames["SongPage"]
        frame.song_result.delete(0, END)
        # now insert the matched results
        for match in songs:
            output_text = str(match)
            frame.song_result.insert(END, output_text)
        conn.close()
        frame.current_artist = artist.strip()
        # now display the song page
        frame.tkraise()

    def search_youtube(self, search):
        search = search.strip()
        query = search.replace(" ", "+")
        # print(query)
        url = "https://www.youtube.com/results?search_query=" + query
        webbrowser.open(url)

    def populate_recommendation_page(self, song_ids):
        frame = self.frames["RecommendPage"]
        # first, delete the previous recommendations
        frame.recommend_results.delete(0, END)

        conn = sqlite3.connect('songs_subset.db')
        cursor = conn.cursor()
        for id in song_ids:
            cursor.execute("""SELECT COALESCE(artist_name, '') || ', ' || COALESCE(title, '') as song FROM songs
                              WHERE "index" = ?""", (id,))
            song = cursor.fetchone()[0]
            frame.recommend_results.insert(END, song)

        conn.close()
        frame.tkraise()








class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Welcome to the Song Recommendation App", font=controller.title_font)
        label.pack(side="top", fill="x")

        button1 = tk.Button(self, text="Search for an artist",
                            command=lambda: controller.show_frame("SearchPage"))
        button1.pack()


class SearchPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.artist_list = self.getArtistNames()
        self.controller = controller
        self.search_result = tk.Listbox(self)
        self.search_result.config(width=75, height=5)
        self.search_result.place(relx=.5, rely=.65, anchor=CENTER )
        scrollbar = Scrollbar(self)
        scrollbar.pack(side=RIGHT, fill=Y)
        label = tk.Label(self, text="SEARCH ARTISTS", font=controller.title_font)
        label.pack(side="top", fill="x")

        # OPTIONS = self.artist_list[:1000]
        # variable = StringVar(self)
        # variable.set(OPTIONS[0])
        # drop_down = OptionMenu(self, variable, *OPTIONS)
        # drop_down.place(x=200, y=100)
        search_field = Entry(self)
        search_field.place(relx=.5, y=100, anchor=CENTER)
        search_button = tk.Button(self, text="Search for Artist",
                                  command=lambda: self.searchArtists(search_field.get()))

        search_button.place(relx=.5, y=75, anchor=CENTER)

        # attach scroll bar to search results box
        self.search_result.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.search_result.yview)
        artist_select_button = tk.Button(self, text="View this artist's available songs",
                            command=lambda: controller.display_artist_songs(self.search_result.selection_get()))
        artist_select_button.place(relx=.5, rely=.85, anchor=CENTER)

        button1 = tk.Button(self, text="return to main menu",
                            command=lambda: controller.show_frame("StartPage"))
        button1.place(relx=.5, rely=.95, anchor=CENTER)

    def getArtistNames(self):
        conn = sqlite3.connect('songs_subset.db')
        conn.row_factory = lambda cursor, row: row[0]
        cursor = conn.cursor()
        cursor.execute("""SELECT DISTINCT(artist_name) from songs ORDER BY artist_name""")
        artists = cursor.fetchall()
        # print(artists[:100])
        conn.close()
        return artists

    def searchArtists(self, search):
        conn = sqlite3.connect('songs_subset.db')
        conn.row_factory = lambda cursor, row: row[0]
        cursor = conn.cursor()
        # print("we got HERE!")
        cursor.execute("""SELECT DISTINCT(artist_name) from songs WHERE artist_name like ? ORDER BY artist_name""",
                       ('%' + search + '%',))
        artists = cursor.fetchall()
        # print(artists)
        # first reset the search results field
        self.search_result.delete(0, END)
        # now insert the matched results
        for match in artists:
                output_text = str(match) + " "
                self.search_result.insert(END, output_text)
        conn.close()


class SongPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        # this holds the current artist whose songs we are viewing
        self.current_artist = None
        self.song_result = tk.Listbox(self)
        self.song_result.config(width=75, height=10)
        self.song_result.place(relx=.5, rely=.4, anchor=CENTER)
        scrollbar = Scrollbar(self)
        scrollbar.pack(side=RIGHT, fill=Y)
        label = tk.Label(self, text="Songs for this artist:", font=controller.title_font)
        label.pack(side="top", fill="x")

        # attach scroll bar to search results box
        self.song_result.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.song_result.yview)
        song_select_button = tk.Button(self, text="Find recommendations similar to this song",
                                         command=lambda: song_predictor.get_recommendations(self.song_result.selection_get(), self.current_artist))
        song_select_button.place(relx=.7, rely=.75, anchor=CENTER)

        youtube_search_button = tk.Button(self, text="Search this song on youtube",
                                       command=lambda: controller.search_youtube(self.current_artist + " " + self.song_result.selection_get()))

        youtube_search_button.place(relx=.2, rely=.75, anchor=CENTER)

        button1 = tk.Button(self, text="return to Artist search",
                            command=lambda: controller.show_frame("SearchPage"))
        button1.place(relx=.5, rely=.9, anchor=CENTER)

class RecommendPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        # this holds the current artist whose songs we are viewing
        self.current_song_id = None
        self.recommend_results = tk.Listbox(self)
        self.recommend_results.config(width=75, height=10)
        self.recommend_results.place(relx=.5, rely=.4, anchor=CENTER)
        scrollbar = Scrollbar(self)
        scrollbar.pack(side=RIGHT, fill=Y)
        label = tk.Label(self, text="Recommendations for this song:", font=controller.title_font)
        label.pack(side="top", fill="x")

        # attach scroll bar to search results box
        self.recommend_results.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.recommend_results.yview)

        youtube_search_button = tk.Button(self, text="Listen to this song on youtube",
                                          command=lambda: controller.search_youtube(self.recommend_results.selection_get()))

        youtube_search_button.place(relx=.5, rely=.75, anchor=CENTER)

        button1 = tk.Button(self, text="return to Artist search",
                            command=lambda: controller.show_frame("SearchPage"))
        button1.place(relx=.5, rely=.9, anchor=CENTER)


song_predictor = SongPredictor()
song_predictor.main_menu.mainloop()