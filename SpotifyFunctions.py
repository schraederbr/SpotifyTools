# requires SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI
# in environment variables.
# SPOTIPY_REDIRECT_URI must be: https://schraederbr.github.io/
# SPOTIPY_REDIRECT_URI

import spotipy
# import json
# import os
# import requests
from spotipy.oauth2 import SpotifyOAuth

scope = "user-library-read streaming user-read-playback-state user-modify-playback-state user-read-currently-playing " \
        "app-remote-control user-library-modify user-follow-modify playlist-modify-private user-top-read"

global sp
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))


# this could be cleaned up by making a function for going through the devices
def start_playback():
    device_response = sp.devices()
    for d in device_response["devices"]:
        if d["is_active"] and not d["is_restricted"]:
            sp.start_playback()


def pause_playback():
    device_response = sp.devices()
    for d in device_response["devices"]:
        if d["is_active"] and not d["is_restricted"]:
            sp.pause_playback()


# Add a check to make sure the user wants to add the song,
# list the name of the song that was found
def add_song_to_queue():
    song_to_search = input("Enter a song to add to queue: ")
    search_response = sp.search(song_to_search, 1, 0, "track", None)
    track_uri = "spotify:track:7Bmd0vPLxSyFFLH7VXm7T2"
    for t in search_response['tracks']['items']:
        track_uri = t['uri']
    device_response = sp.devices()
    for d in device_response["devices"]:
        if d["is_active"] and not d["is_restricted"]:
            # sp.start_playback()
            sp.add_to_queue(track_uri)
            print("'" + t['name'] + "'" + " by: " + "'" + t['artists'][0]['name'] + "'"
                  + " has been added to your queue")


def print_top_tracks():
    how_many = input("How many top tracks to display?")
    if how_many.isdigit():
        top_track_response = sp.current_user_top_tracks(how_many, 0, "long_term")
        for t in top_track_response['items']:
            print("'" + t['name'] + "'" + " by: " + "'" + t['artists'][0]['name'] + "'")
    else:
        print('invalid input')
        my_main()


# doesn't work at the moment
def re_login():
    global sp
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(show_dialog='true', scope=scope))


def my_main():
    while True:
        function_to_start = input(
            '1 to play. 2 to pause. 3 to add a song to queue. 4 to print top tracks\n'
            '5 to change account. exit to quit\n')
        if function_to_start == '1':
            start_playback()
        elif function_to_start == '2':
            pause_playback()
        elif function_to_start == '3':
            add_song_to_queue()
        elif function_to_start == '4':
            print_top_tracks()
        elif function_to_start == '5':
            re_login()
        elif function_to_start == 'exit':
            break
        else:
            print('Unrecognized command')


my_main()
