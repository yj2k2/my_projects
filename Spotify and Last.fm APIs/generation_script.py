import spotipy #This library is for authentication to the Spotify API
from spotipy.oauth2 import SpotifyClientCredentials #Same
from spotipy.oauth2 import SpotifyOAuth #Same
import os #This library is for environment variables
import requests #This library is for making HTTP requests
import time

#These are the environment variables
os.environ['SPOTIPY_CLIENT_ID'] = '477d9702016f4f768c4ae6107993e493'
os.environ['SPOTIPY_CLIENT_SECRET'] = '70636d71c3b947ba9ba51c6fb007158d'
os.environ['LASTFM_API_KEY'] = '50ac41faead378f0e4e91a45d9d56a56'
os.environ['LASTFM_SHARED_SECRET'] = '20c8fe319f22f83bddbd29f076815bd5'
os.environ['SPOTIPY_REDIRECT_URI'] = 'http://localhost:8080/callback'


#Here we do the authentication (read about scope in the Spotify API Documentation)
try:
	spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
	sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope="playlist-modify-public"))
except Exception as e:
	print("Sorry, an error occured when trying to connect to the Spotify API.")
	time.sleep(5)
	os._exit(0)

try:
	response = requests.post(f"http://ws.audioscrobbler.com/2.0/?method=auth.gettoken&api_key={os.getenv('LASTFM_API_KEY')}&format=json")
	token = response.json()['token']
except Exception as e:
	print("Sorry, an error occured when trying to connect to the Last.fm API.")
	time.sleep(5)
	os._exit(0)


"""
url  = f"https://www.last.fm/api/auth/?api_key={api_key}&token={token}"
print("Follow this link to grant access : ", url)
"""

#This is a function for verifying if a track URI is valid in Spotify
def verifyURI(trackURI):
	try:
		track = spotify.track(trackURI)
		return True
	except Exception as e:
		return False

#This is a function that extracts top tags of a specific artist from Last.fm
def extractTags(artist):
	try:
		response = requests.post(f"http://ws.audioscrobbler.com/2.0/?method=artist.getTopTags&api_key={os.getenv('LASTFM_API_KEY')}&artist={artist}&user=RJ&format=json")
		tags = response.json()
		tags = tags['toptags']['tag']
	except Exception as e:
		print("Sorry, an error occured when trying to extract tags.")
		time.sleep(5)
		os._exit(0)

	list_tags = []

	try : 
		for case in range(len(tags)):
			list_tags.append(tags[case]['name'])
	except Exception as e:
		print("Sorry, an error occured when adding tags to a list.")
		time.sleep(5)
		os._exit(0)


	return list_tags


#This is a function i use to refine the Last.fm suggestions by comparing artist tags
def filterSimilarTracks(original_artist, json_similar_tracks, user_id, playlist_id):
	orig_art_tags = set(extractTags(original_artist))
	len_orig_set = len(orig_art_tags)
	listURI = []

	try:
		for key, value in json_similar_tracks.items():
			art_tags = set(extractTags(value))
			len_set = len(art_tags)

			common_tags = orig_art_tags.intersection(art_tags)
			count_common = len(common_tags)

			if (count_common > 2) and (count_common > (min(len_orig_set, len_set) - count_common)):
				uri = getTrackURI(key, value)
				listURI.append(uri)
	except Exception as e:
		print("Sorry, an error occured when choosing similar tracks.")
		time.sleep(5)
		os._exit(0)


	try:
		validURIs = []
		for index, trackURI in enumerate(listURI):
			if (verifyURI(trackURI) == True):
				validURIs.append(trackURI)
	except Exception as e:
		print("Sorry, an error occured when verifying the list of URIs.")
		time.sleep(5)
		os._exit(0)
		
	try:
		addPlaylistTracks(user_id, playlist_id, validURIs)
	except Exception as e:
		print("Sorry, an error occured when adding the tracks to the new playlist.")
		time.sleep(5)
		os._exit(0)




#This function is for getting similar tracks to our songs via the Last.fm API
def getSimilarTracks(api_key=os.getenv('LASTFM_API_KEY')) :
	similar_tracks = {}
	try :
		artist = str(input("Give me the artist name : "))
		track = str(input("Give me the track name : "))
	except Exception as e:
		print("Sorry, an error occured when getting the name of the track/artist.")
		time.sleep(5)
		os._exit(0)

	#Here we construct the url and give the artist name and track name we just recuperated
	try:
		limit = str(input("Give me the limit of similar tracks :"))
		url = f"http://ws.audioscrobbler.com/2.0/?method=track.getsimilar&artist={artist}&track={track}&autocorrect=1&api_key={api_key}&format=json&limit={limit}"
		results = requests.get(url).json()
	except Exception as e:
		print("Sorry, an error occured when trying to get similar tracks from Last.fm API.")
		time.sleep(5)
		os._exit(0)


	#After getting the tracks, we take from them their titles and their artist names only
	try:
		for track in results['similartracks']['track']:
			track_name = track['name']
			artist_name = track['artist']['name']
			similar_tracks[track_name] = artist_name #Map the data
	except Exception as e:
		print("Sorry, an error occured when mapping the data of similar tracks.")
		time.sleep(5)
		os._exit(0)

	return artist, similar_tracks

#This is a function that gets a playlist's information
def getPlaylist(playlist_name):
	try:
		user_playlists = sp.current_user_playlists() #Here we get all the playlists of the user
	except Exception as e:
		print("Sorry, an error occured when trying to get the playlists of the user.")
		time.sleep(5)
		os._exit(0)
	try:
		for playlist in user_playlists['items']:
			if playlist['name'] == playlist_name:
				return playlist
	except Exception as e:
		print("Sorry, an error occured when searching for the new playlist by its name.")
		time.sleep(5)
		os._exit(0)

#This function is for getting the id of the new playlist we create
def getPlaylistID(playlist_name):
	try:
		playlist = getPlaylist(playlist_name)
		return playlist['id']
	except Exception as e:
		print("Sorry, an error occured when trying to get the ID of the new playlist.")
		time.sleep(5)
		os._exit(0)


#This function is for getting the total number of tracks in a playlist
def getPlaylistTotal(playlist_name):
	try:
		playlist = getPlaylist(playlist_name)
		return playlist['tracks']['total']
	except Exception as e:
		print("Sorry, an error occured when trying to get the total number of tracks of the new playlist.")
		time.sleep(5)
		os._exit(0)

#This function is for creating new playlists (this is where the scope is used for example)
def createPlaylist(playlist_name):
	try:
		user_profile = sp.me()
		user_id = user_profile["id"] #Get my id
	except Exception as e:
		print("Sorry, an error occured when trying to get the ID of the user.")
		time.sleep(5)
		os._exit(0)
	try:
		description = str(input("Give me the new playlist's description : "))
		sp.user_playlist_create(user_id, playlist_name, public=True, collaborative=False, description=description)
	except Exception as e:
		print("Sorry, an error occured when trying to create the new playlist.")
		time.sleep(5)
		os._exit(0)



#This function is made to get the URI of a track in Spotify. We will use it to add tracks to a playlist
def getTrackURI(track_name, artist_name): 
	try:
		tracklist = spotify.search(q=f"https://api.spotify.com/v1/search?track={track_name}&artist={artist_name}", limit=15, type="track")
	except Exception as e:
		print("Sorry, an error occured when trying to search for the track from the Spotify API.")
		time.sleep(5)
		os._exit(0)

	tracks = {}
	uri = ""
	popularity = 0

	#Here we take the most popular example
	try:
		for track in tracklist['tracks']['items']:
				track_uri = track['uri']
				track_popularity = track['popularity']
				track_artist = track['artists'][0]['name']
				track_name = track['name'].upper()
				if track_artist == artist_name and track_name.find("LIVE") == -1:
					tracks[track_uri] = track_popularity
	except Exception as e:
		print("Sorry, an error occured when trying to filter the search results from the Spotify API.")
		time.sleep(5)
		os._exit(0)

	try:
		for key, value in tracks.items():
			if value > popularity:
				uri = key
				popularity = value
	except Exception as e:
		print("Sorry, an error occured when trying to get the right example of the desired track from the Spotify API.")
		time.sleep(5)
		os._exit(0)
	
	return uri

#In this function, we add the tracks to our new playlist by passing the previous list as a parameter
def addPlaylistTracks(user_id, playlist_id, listURI):
	try:
		sp.user_playlist_add_tracks(user=user_id, playlist_id=playlist_id, tracks=listURI)
	except Exception as e:
		print("Sorry, an error occured when trying to add the new tracks to the playlist.")
		time.sleep(5)
		os._exit(0)


#In the main, we follow the logic of the whole process by using all of our functions and variables
def main():
	try:
		original_artist, similar_tracks = getSimilarTracks()
		playlist_name = str(input("Give me the playlist name : "))
		createPlaylist(playlist_name)
		user_profile = sp.me()
		user_id = user_profile["id"]
		playlist_id = getPlaylistID(playlist_name)
		filterSimilarTracks(original_artist, similar_tracks, user_id, playlist_id)
		print(f"The new playlist contains {getPlaylistTotal(playlist_name)} tracks")
	except Exception as e:
		print("Sorry, an error occured in the main function.")
		time.sleep(5)
		os._exit(0)


main()