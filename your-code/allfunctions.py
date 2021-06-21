#Importing libraries
###############General#################
import pandas as pd

############WebScraping#############


#############Spotify#################
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from Credentials import Client_ID, Client_Secret



#Webscraping#######################################
 
#Spotify API######################################

client_credentials_manager = SpotifyClientCredentials(client_id=Client_ID, client_secret=Client_Secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

#Machine Learning#################################




#################### Function to get the uri of a song name ######################


def get_uri_of_song(song_name):
    results = sp.search(q=song_name, limit=1)
    uri = results["tracks"]["items"][0]["uri"]
    return uri

########## Function to get the audio features of a song as a dictionary ###########
def get_audio_features_of_song(song_name):
    audio_features = sp.audio_features(song_name["tracks"]["items"][0]["uri"])[0]
    audio_features = { key: [audio_features[key]] for key in list(audio_features.keys()) }
    return audio_features

################## Function to get the songs from a playlist ####################
''' Text '''
def get_playlist_tracks(username, playlist_id): #username is always "spotify" and playlist_id is the id in the link.
    results = sp.user_playlist_tracks(username, playlist_id)
    tracks = results["items"]
    while results["next"]:
        results = sp.next(results)
        tracks.extend(results["items"])
    return tracks

############ Function to get audio features from uri###############
def get_audio_features_from_list_of_uris(list_with_uris):#
    '''Text'''
    list_with_dicts_of_audio_features = []
    for i in range(len(list_with_uris)):
        list_with_dicts_of_audio_features.append(sp.audio_features(list_with_uris[i]))
        #seconds = list(np.random.choice(range(1,6),1))[0]
        #sleep(seconds)
    return list_with_dicts_of_audio_features

#########Function to get a dict with all audio features from each song's audio feature#######
def create_dict_with_audiofeatures_for_all_songs(list_with_audio_features):
    '''Text'''
    features = {key: [] for key in list_with_audio_features[0][0]}

    for i in range(len(list_with_audio_features)):
        for key in features.keys():
            features[key].append(list_with_audio_features[i][0][key])
            
    return features

######### Function to get the dataframe from a playlist id###############
def get_dataframe_from_playlist_id(playlist_id):
    ''' Text '''
    playlist =  get_playlist_tracks("spotify", playlist_id) 
    
    playlist_uri = [] 
    playlist_artist_names = [] 
    playlist_song_names = []

    for i in range(len(playlist)):
        playlist_uri.append(playlist[i]["track"]["uri"]) #The i is the name of the song in the playlist.
        playlist_artist_names.append(playlist[i]["track"]["artists"][0]["name"])
        playlist_song_names.append(playlist[i]["track"]["name"])
    
    playlist_audio_features = get_audio_features_from_list_of_uris(playlist_uri)
    playlist_dict_audiofeature = create_dict_with_audiofeatures_for_all_songs(playlist_audio_features)
    df_playlist = pd.DataFrame(playlist_dict_audiofeature)
    df_artist_names = pd.DataFrame(playlist_artist_names, columns=["Artist_Names"])
    df_song_names = pd.DataFrame(playlist_song_names, columns=["Song_Names"])
    x = pd.concat([df_song_names, df_artist_names], axis=1)
    y = pd.concat([x, df_playlist], axis=1)
    return y

################Function to get the mega dataframe from a list of playlist ids############
'''Input: List with the playlist ids
Output: mega_dataframe with all the audiofeatures.'''
def mega_dataframe_from_playlist_id_list(playlist_id_list):
    mega_dataframe = pd.DataFrame()
    for id in playlist_id_list:
        df = get_dataframe_from_playlist_id(id)
        mega_dataframe = pd.concat([mega_dataframe,df])
    return mega_dataframe

#################Function to get audio features for user input#########
def user_song_audio_featuers(song_input):
    list_uris = []
    list_uris.append(get_uri_of_song(song_input))
    audio_features = get_audio_features_from_list_of_uris(list_uris)
    return audio_features

##################Function to get song input from user###############
def song_input():
    song_input = input("Please enter a song name or artist name: ")
    return song_input

############# Function to create dataframe from dictionary#########
def create_dataframe_from_dictionary(dictionary, columns=None):
    '''
    Input:

    dictionary: dictionary with dataframe values
    columns (opt): list with column names

    Output: Dataframe
    '''
    dataframe = pd.DataFrame(data=dictionary, columns=None)
    return dataframe
    
##########Function to get all information about one song from spotify as a json file###########
def get_all_information_about_song(song_name):
    '''Text'''
    song = sp.search(q=song_name, limit=1)
    return song

##################### Function to get id of a song ##############################
#'''Text'''
#def get_song_id(song_name):
#    results = sp.search(q=song_name, limit=1)
#    id = results['tracks']['items'][0]['id']
#    return id

############### Function to get the artist from a track#################
#'''Text'''
#def get_artists_from_track(track):
#    return [artist["name"] for artist in track["artists"]]

############# Function to get the artist from playlist##############
#'''Text'''
#def get_artists_from_playlist(playlist_id):
#    tracks_from_playlist = get_playlist_tracks("spotify", playlist_id)
#    return list(set(artist for subset in [get_artists_from_track(track["track"]) for track in tracks_from_playlist] for artist in subset))

def get_artists_name_from_song(song_name):
    song_information = get_all_information_about_song(song_name)
    Artist_Names = song_information["tracks"]["items"][0]["artists"][0]["name"]
    return Artist_Names

